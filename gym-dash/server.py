#!/usr/bin/env python3
"""
Gym Dash — local server.
Serves all static files AND writes daily JSON files via POST /api/save-day.

Usage:
    python server.py

Then open:  http://localhost:8181
Stop:       Ctrl + C
"""
import http.server
import json
import os
import socketserver
from datetime import date

PORT = 8181
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data')


class GymHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)

    # ── CORS pre-flight ──────────────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    # ── POST router ──────────────────────────────────────────────────────────
    def do_POST(self):
        if   self.path == '/api/save-day':    self._save_day()
        elif self.path == '/api/save-config': self._save_config()
        else:
            self.send_response(404); self.end_headers()

    def _save_day(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            data   = json.loads(body)

            day_str  = data.get('date', str(date.today()))
            filename = day_str + '.json'
            os.makedirs(DATA, exist_ok=True)

            with open(os.path.join(DATA, filename), 'w') as fh:
                json.dump(data, fh, indent=2)

            # Keep manifest.json in sync
            mpath = os.path.join(DATA, 'manifest.json')
            manifest = json.load(open(mpath)) if os.path.exists(mpath) else []
            if filename not in manifest:
                manifest.append(filename)
            manifest.sort(reverse=True)
            with open(mpath, 'w') as fh:
                json.dump(manifest, fh, indent=2)

            self._json(200, {'ok': True, 'file': filename})
        except Exception as exc:
            self._json(500, {'error': str(exc)})

    def _save_config(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            data   = json.loads(body)
            cpath  = os.path.join(BASE, 'config.json')
            with open(cpath, 'w') as fh:
                json.dump(data, fh, indent=2)
            self._json(200, {'ok': True})
        except Exception as exc:
            self._json(500, {'error': str(exc)})

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _json(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self._cors()
        self.send_header('Content-Type',   'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, *_):
        pass  # suppress per-request console noise


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('', PORT), GymHandler) as srv:
        print(f'\n  GYM DASH  ->  http://localhost:{PORT}')
        print(f'  Data dir  ->  {DATA}')
        print(f'  Stop      ->  Ctrl + C\n')
        srv.serve_forever()
