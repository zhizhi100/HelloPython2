object frminstall: Tfrminstall
  Left = 755
  Top = 346
  BorderIcons = [biSystemMenu]
  BorderStyle = bsDialog
  Caption = #19968#38190#23433#35013#37329#19977#21161#25163
  ClientHeight = 244
  ClientWidth = 389
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -15
  Font.Name = #24494#36719#38597#40657
  Font.Style = []
  OldCreateOrder = False
  Position = poScreenCenter
  PixelsPerInch = 96
  TextHeight = 20
  object lbl1: TLabel
    Left = 8
    Top = 8
    Width = 240
    Height = 20
    Caption = #19968#38190#23433#35013#37329#19977#21161#25163#65292#36827#34892#20197#19979#25805#20316#65306
  end
  object grp1: TGroupBox
    Left = 10
    Top = 32
    Width = 367
    Height = 161
    TabOrder = 0
    object lbl2: TLabel
      Left = 8
      Top = 136
      Width = 348
      Height = 17
      Caption = #26432#27602#36719#20214#21487#33021#20250#38459#27490#23433#35013#26381#21153#65292#35831#20801#35768#23433#35013#25110#26242#26102#20851#38381#26432#27602#36719#20214#12290
      Font.Charset = ANSI_CHARSET
      Font.Color = clRed
      Font.Height = -12
      Font.Name = #24494#36719#38597#40657
      Font.Style = []
      ParentFont = False
    end
    object chkquick: TCheckBox
      Left = 17
      Top = 24
      Width = 185
      Height = 17
      Caption = #21019#24314#26700#38754#24555#25463#26041#24335
      Checked = True
      State = cbChecked
      TabOrder = 0
    end
    object chkreg: TCheckBox
      Left = 17
      Top = 53
      Width = 185
      Height = 17
      Caption = #23433#35013#37329#19977#21161#25163#21518#21488#26381#21153
      Checked = True
      State = cbChecked
      TabOrder = 1
    end
    object chkstart: TCheckBox
      Left = 17
      Top = 83
      Width = 185
      Height = 17
      Caption = #21551#21160#37329#19977#21161#25163#21518#21488#26381#21153
      Checked = True
      State = cbChecked
      TabOrder = 2
    end
    object chkieproxy: TCheckBox
      Left = 17
      Top = 112
      Width = 105
      Height = 17
      Caption = #37197#32622'IE'#20195#29702
      Checked = True
      State = cbChecked
      TabOrder = 3
    end
    object chklocal: TCheckBox
      Left = 119
      Top = 112
      Width = 117
      Height = 17
      Caption = #26816#26597#26412#22320#26381#21153
      TabOrder = 4
    end
    object chkproxy: TCheckBox
      Left = 233
      Top = 112
      Width = 113
      Height = 17
      Caption = #26816#26597#20195#29702#26381#21153
      TabOrder = 5
    end
  end
  object btnok: TButton
    Left = 296
    Top = 200
    Width = 83
    Height = 33
    Caption = #21462#28040'(&C)'
    TabOrder = 1
    OnClick = btnokClick
  end
  object btnyes: TButton
    Left = 208
    Top = 200
    Width = 83
    Height = 33
    Caption = #30830#23450'(&O)'
    TabOrder = 2
    OnClick = btnyesClick
  end
end
