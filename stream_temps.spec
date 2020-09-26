# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['stream_temps.py'],
             pathex=['/Users/konze/Programming/stream_temps'],
             binaries=[],
             datas=[],
             hiddenimports=['PIL._tkinter_finder'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += Tree('./root_dir', prefix='root_dir')
a.datas += Tree('./templates', prefix='templates')
a.datas += Tree('./images', prefix='images')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='stream_temps',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='stream_temps')

