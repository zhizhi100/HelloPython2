unit uQRCode;

interface

uses
  Windows, Graphics;


type
   pPTIMAGESTRUCT=^PTIMAGESTRUCT  ;
   PTIMAGESTRUCT = record
        dwWidth  :     DWORD;
        dwHeight :     DWORD;
        pBits :        PByte ;
        pPalette:      PByte;
        wBitsPerPixel: Smallint
   end;
   procedure PtInitImage(pImage: pPTIMAGESTRUCT);stdcall; far; external 'PtImageRW.dll' name 'PtInitImage';
   procedure PtShowImage( pImage: pPTIMAGESTRUCT; hDc: HDC; StartX, StartY: Integer; Scale: Double);stdcall; far; external 'PtImageRW.dll' name 'PtShowImage';
   Function PtLoadImage(fileName : String; pImage : pPTIMAGESTRUCT;  FrameIndex: DWORD) : Integer;stdcall; far; external 'PtImageRW.dll' name 'PtLoadImage';
   Function PtSaveImage( fileName : String; pImage : pPTIMAGESTRUCT) : Integer;stdcall; far; external 'PtImageRW.dll' name 'PtSaveImage';
   Function PtCreateImage( pImage : pPTIMAGESTRUCT; ImageSize: DWORD; PaletteSize:DWORD ) : Integer;stdcall; far; external 'PtImageRW.dll' name 'PtCreateImage';
   procedure PtFreeImage(pImage: pPTIMAGESTRUCT);stdcall; far; external 'PtImageRW.dll' name 'PtFreeImage';

   type
        pPTQRENCODESTRUCT=^PTQRENCODESTRUCT;
        PTQRENCODESTRUCT = record
        pData :              PChar ;
        nDataLength :        Integer ;
        wVersion:            Smallint ;
        wMaskNumber:         Smallint ;
        wEccLevel  :         Smallint	;
        wModule  :           Smallint	;
        wGroupTotal :        Smallint	;
        wGroupIndex :        Smallint	;
        wLeftSpace :         Smallint	;
        wRightSpace :        Smallint	;
        wTopSpace :          Smallint	;
        wBottomSpace :       Smallint	;
   end;
        procedure PTQREncodeInit(pEncode: pPTQRENCODESTRUCT) ;stdcall; far; external 'PtQREncode.dll' name 'PtQREncodeInit';
        function PtQREncode(pEncode: pPTQRENCODESTRUCT; pImage : pPTIMAGESTRUCT): Integer;stdcall; far; external 'PtQREncode.dll' name 'PtQREncode';
        function PtQREncodeToImage(pEncode: pPTQRENCODESTRUCT; pImage: pPTIMAGESTRUCT; StartX: Integer; StartY: Integer): Integer;stdcall; far; external 'PtQREncode.dll' name 'PtQREncodeToImage';


        procedure CreateQRCode(ACode: string; AVersion, AEccLevel, AModule: SmallInt;path:String);
implementation
procedure CreateQRCode(ACode: string; AVersion, AEccLevel, AModule: SmallInt;path:String);
var
        ret: integer;
        m_image: PTIMAGESTRUCT;
        m_encode: PTQRENCODESTRUCT;
begin
        PtInitImage(@m_image);
        PtQREncodeInit(@m_encode);

        m_encode.pData := pChar(ACode);
        m_encode.nDataLength := lstrlen(m_encode.pData);
        m_encode.wVersion := AVersion;
        m_encode.wEccLevel := AEccLevel;
        m_encode.wModule := AModule;
        m_encode.wLeftSpace := 0;
        m_encode.wRightSpace := 0;
        m_encode.wTopSpace := 0;
        m_encode.wBottomSpace := 0;

        ret := PtQREncode(@m_encode, @m_image);

         If ret = $00000001 Then
         begin
                ret := PtSaveImage( path, @m_image);
               
         end;
         PtFreeImage(@m_image);
end;

end.
