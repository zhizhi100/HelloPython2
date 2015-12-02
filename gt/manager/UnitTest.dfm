object frmtest: Tfrmtest
  Left = 867
  Top = 616
  Width = 503
  Height = 337
  Caption = #27979#35797
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -13
  Font.Name = #23435#20307
  Font.Style = []
  Menu = mm1
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object lbledtcmd: TLabeledEdit
    Left = 8
    Top = 32
    Width = 465
    Height = 21
    EditLabel.Width = 39
    EditLabel.Height = 13
    EditLabel.Caption = #21629#20196#34892
    ImeName = #20013#25991'('#31616#20307') - '#25628#29399#25340#38899#36755#20837#27861
    TabOrder = 0
  end
  object mm1: TMainMenu
    Left = 24
    Top = 16
    object N1: TMenuItem
      Caption = #27979#35797
      object N2: TMenuItem
        Caption = #23433#35013#26381#21153
        OnClick = N2Click
      end
      object N3: TMenuItem
        Caption = #21368#36733#26381#21153
        OnClick = N3Click
      end
      object N4: TMenuItem
        Caption = #26597#35810#26381#21153
        OnClick = N4Click
      end
      object N5: TMenuItem
        Caption = #21551#21160#26381#21153
        OnClick = N5Click
      end
      object N6: TMenuItem
        Caption = #20572#27490#26381#21153
        OnClick = N6Click
      end
      object cmd1: TMenuItem
        Caption = 'cmd'
        OnClick = cmd1Click
      end
    end
    object N7: TMenuItem
      Caption = #20854#20182
      object ini1: TMenuItem
        Caption = 'ini'#20889
        OnClick = ini1Click
      end
    end
  end
end
