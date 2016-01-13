object frmlic: Tfrmlic
  Left = 288
  Top = 368
  Width = 432
  Height = 350
  BorderIcons = [biSystemMenu]
  Caption = #25480#26435#20449#24687
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -16
  Font.Name = #24494#36719#38597#40657
  Font.Style = []
  OldCreateOrder = False
  Position = poScreenCenter
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 21
  object lbl1: TLabel
    Left = 36
    Top = 136
    Width = 48
    Height = 21
    Caption = #29305#24449#30721
    Visible = False
  end
  object Label1: TLabel
    Left = 20
    Top = 276
    Width = 64
    Height = 21
    Caption = #35797#29992#23494#38053
  end
  object img1: TImage
    Left = 20
    Top = 64
    Width = 200
    Height = 200
  end
  object lbl2: TLabel
    Left = 240
    Top = 80
    Width = 133
    Height = 25
    Caption = #25195#19968#25195#30003#35831#35797#29992
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -19
    Font.Name = #24494#36719#38597#40657
    Font.Style = []
    ParentFont = False
  end
  object Label2: TLabel
    Left = 232
    Top = 176
    Width = 114
    Height = 25
    Caption = #21487#37325#22797#30003#35831#21727
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -19
    Font.Name = #24494#36719#38597#40657
    Font.Style = []
    ParentFont = False
  end
  object Label3: TLabel
    Left = 336
    Top = 224
    Width = 38
    Height = 25
    Caption = #65306#65289
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -19
    Font.Name = #24494#36719#38597#40657
    Font.Style = []
    ParentFont = False
  end
  object Label4: TLabel
    Left = 264
    Top = 128
    Width = 80
    Height = 27
    Caption = #37329#19977#21161#25163
    Font.Charset = ANSI_CHARSET
    Font.Color = clRed
    Font.Height = -20
    Font.Name = #24494#36719#38597#40657
    Font.Style = [fsBold]
    ParentFont = False
  end
  object edtfeature: TEdit
    Left = 36
    Top = 160
    Width = 381
    Height = 29
    Color = cl3DLight
    ImeName = #20013#25991'('#31616#20307') - '#25628#29399#25340#38899#36755#20837#27861
    ReadOnly = True
    TabOrder = 0
    Visible = False
  end
  object edtkey: TEdit
    Left = 96
    Top = 272
    Width = 233
    Height = 29
    ImeName = #20013#25991'('#31616#20307') - '#25628#29399#25340#38899#36755#20837#27861
    TabOrder = 1
  end
  object btngetkey: TButton
    Left = 20
    Top = 208
    Width = 129
    Height = 33
    Caption = #30003#35831#35797#29992#23494#38053
    TabOrder = 2
    Visible = False
    OnClick = btngetkeyClick
  end
  object btn1: TButton
    Left = 272
    Top = 208
    Width = 129
    Height = 33
    Caption = #36141#20080#27491#24335#25480#26435
    TabOrder = 3
    Visible = False
    OnClick = btn1Click
  end
  object btn2: TButton
    Left = 334
    Top = 268
    Width = 65
    Height = 33
    Caption = #26816#39564
    TabOrder = 4
    OnClick = btn2Click
  end
  object pnl1: TPanel
    Left = 18
    Top = 8
    Width = 381
    Height = 49
    BevelInner = bvLowered
    Caption = #24744#23578#26410#30003#35831#35797#29992#25480#26435#65281
    Font.Charset = ANSI_CHARSET
    Font.Color = clRed
    Font.Height = -21
    Font.Name = #23435#20307
    Font.Style = [fsBold]
    ParentFont = False
    TabOrder = 5
  end
end
