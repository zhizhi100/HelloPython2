object frmlic: Tfrmlic
  Left = 305
  Top = 506
  Width = 432
  Height = 291
  BorderIcons = [biSystemMenu]
  Caption = #25480#26435#20449#24687
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -16
  Font.Name = #23435#20307
  Font.Style = []
  OldCreateOrder = False
  Position = poScreenCenter
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 16
  object lbl1: TLabel
    Left = 20
    Top = 8
    Width = 48
    Height = 16
    Caption = #29305#24449#30721
  end
  object Label1: TLabel
    Left = 20
    Top = 69
    Width = 64
    Height = 16
    Caption = #35797#29992#23494#38053
  end
  object lbl2: TLabel
    Left = 20
    Top = 126
    Width = 96
    Height = 16
    Caption = #35797#29992#25480#26435#26399#38480
  end
  object edtfeature: TEdit
    Left = 20
    Top = 32
    Width = 381
    Height = 27
    Color = cl3DLight
    ReadOnly = True
    TabOrder = 0
  end
  object edtkey: TEdit
    Left = 20
    Top = 88
    Width = 309
    Height = 28
    TabOrder = 1
  end
  object btngetkey: TButton
    Left = 20
    Top = 208
    Width = 129
    Height = 33
    Caption = #30003#35831#35797#29992#23494#38053
    TabOrder = 2
    OnClick = btngetkeyClick
  end
  object btn1: TButton
    Left = 272
    Top = 208
    Width = 129
    Height = 33
    Caption = #20351#29992#27491#24335#25480#26435
    TabOrder = 3
  end
  object btn2: TButton
    Left = 334
    Top = 83
    Width = 65
    Height = 33
    Caption = #26816#39564
    TabOrder = 4
    OnClick = btn2Click
  end
  object pnl1: TPanel
    Left = 20
    Top = 152
    Width = 381
    Height = 49
    BevelInner = bvLowered
    Caption = #24744#23578#26410#30003#35831#35797#29992#23494#38053#65281
    Font.Charset = ANSI_CHARSET
    Font.Color = clRed
    Font.Height = -21
    Font.Name = #23435#20307
    Font.Style = [fsBold]
    ParentFont = False
    TabOrder = 5
  end
end
