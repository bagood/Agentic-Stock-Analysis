import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class AuthenticationBootstrapTests(unittest.TestCase):
    def test_imports_only_credentials_and_preserves_existing_volume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            host, home = root/'host', root/'volume'
            host.mkdir()
            home.mkdir()
            (host/'auth.json').write_text('synthetic-credential')
            (host/'config.toml').write_text('personal MCP configuration')
            (host/'plugins').mkdir()
            script = Path('docker-entrypoint.sh').read_text().replace('/host-codex', str(host)).replace('/app/.env', str(root/'.env'))
            entry = root/'entry.sh'
            entry.write_text(script)
            env = dict(os.environ, CODEX_HOME=str(home))
            subprocess.run(['sh', str(entry), 'true'], env=env, check=True)
            self.assertEqual([p.name for p in home.iterdir()], ['auth.json'])
            self.assertEqual((home/'auth.json').stat().st_mode & 0o777, 0o600)
            (home/'auth.json').write_text('existing-credential')
            (home/'config.toml').write_text('legacy settings')
            subprocess.run(['sh', str(entry), 'true'], env=env, check=True)
            self.assertEqual((home/'auth.json').read_text(), 'existing-credential')
            self.assertEqual((home/'config.toml').read_text(), 'legacy settings')

    def test_api_key_is_available_to_codex_without_printing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = Path('docker-entrypoint.sh').read_text().replace('/host-codex', str(root/'missing')).replace('/app/.env', str(root/'.env'))
            entry = root/'entry.sh'
            entry.write_text(script)
            env = dict(os.environ, CODEX_HOME=str(root/'home'), OPENAI_API_KEY='synthetic-key', CODEX_API_KEY='')
            result = subprocess.run(['sh', str(entry), 'sh', '-c', 'test "$CODEX_API_KEY" = "$OPENAI_API_KEY"'],
                                    env=env, capture_output=True, check=True)
            self.assertEqual(result.stdout, b'')
            self.assertEqual(result.stderr, b'')
