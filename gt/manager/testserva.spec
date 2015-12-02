# -*- mode: python -*-

block_cipher = None


a = Analysis(['E:\\workspace\\HelloPython2\\gt\\serv\\testserva.py'],
             pathex=['E:\\workspace\\HelloPython2\\gt\\', 'E:\\test\\python'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='testserva',
          debug=False,
          strip=None,
          upx=True,
          console=True )
