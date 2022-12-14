client_gui.py                                                                                       0000664 0001750 0001750 00000015470 14342037315 012173  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   """
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Show the gui used by the client.  It accepts a team and a season.
         When the lookup information button is pressed, a message is sent to the
         server process via a socket.  The server's response is populated into
         the appropriate fields.
"""

import datetime

from breezypythongui import EasyFrame
from codecs import decode
from socket import *

from nba_record_server import ADDRESS
from request import Request
from response import build_response_from_message

BUFSIZE = 1024

FROM_YEAR=1947
today=datetime.date.today()
TO_YEAR=today.year

# list of the fields retreived from the server.
RESULT_FIELDS = ["League", "Season", "Team Name", "Won", "Lost", "Win %",
                 "Playoff Results", "Coach(es)", "Best Player"
                ]

def build_year_list(start_year, end_year):
    """
    Build a list of seasons in the correct format.  For example, 1980-81 or 1999-00.
    param start_year: first part of the first year to include
    param end_year: last part of the last season to include.
    return: list of years in the range
    """
    season_list = []
    for yr in range(end_year-1,start_year-1,-1):
        next = str( (yr+1) % 100 )
        if (len(next)==1):
            next = "0" + next
        current_season = "%s-%s" % (yr,next)
        season_list.append(current_season)

    return season_list

SEASONS=build_year_list(FROM_YEAR, TO_YEAR)

def establish_connection_to_server():
    """
    Connect to the lookup server.
    return: the socket to communite with.
    """
    server_socket = socket(AF_INET, SOCK_STREAM)               # Create a socket
    server_socket.connect(ADDRESS)                             # Connect it to a host
    return server_socket

def send_request(server_socket, request):
    """
    Send the request to the server for a given team and year.
    param server_socket: communication channel
    param request: request object (contains team and year info)
    """
    text_response = str(request) + "\n"
    server_socket.send(bytes(text_response,"ascii"))

def get_response( server_socket ):
    """
    Get the server's response and store it into a season data object.
    param server_socket: Communication channel
    return: Information from the server.
    """
    server_response = decode(server_socket.recv(BUFSIZE), "ascii").split("\n")
    season_data = build_response_from_message(server_response[0]+"\n")
    return season_data



class NbaRecordClientGui(EasyFrame):
    """
    Main class for this module.

    Displays the window and dispatches button clicks.
    """

    def add_gui_line( self, label_text, row_num):
        """
        Add a label <-> text box pair to display the season information.
        param label_text: Label identifying the text
        param row_num: What row on the screen to display the pair in
        return: the textfield object so the value can be updated later.
        """
        self.addLabel(text=label_text,
                      row=row_num,
                      column=0,
                      sticky="NW"
                      )

        return self.addTextField(text="",
                                 row=row_num,
                                 column=1,
                                 sticky="NW"
                                 )

    def add_result_fields(self, fields, start_at_row ):
        """
        Add a group of fields that will be populated with data from the server.
        :param fields:  The list of fields to be added.  This is a list of
                        strings that are used as the labels.
        :param start_at_row: The first row to use.  Each field gets its own
                             row.
        :return: a list of the textbox objects so the screen can be updated.
        """
        result_field_objects = []
        current_row = start_at_row
        for fld in fields:
            current_field = self.add_gui_line( fld, current_row )
            result_field_objects.append(current_field)
            current_row += 1
        return result_field_objects

    def __init__(self):
        """
        Setup widgets on window
        """
        EasyFrame.__init__(self)
        self.setTitle("NBA Season Record Lookup Utility")

        # NBA Team Row (0)
        self.addLabel(text="NBA Team:",
                      row=0,
                      column=0,
                      sticky="NW"
                      )
        team_list = ["Lakers","Pelicans"]
        self.team = self.addCombobox \
            (row = 0,
             column = 1,
             values=team_list,
             text=""
             )
        self.team.set(team_list[0])

        self.addLabel(text="",
                      row=0,
                      column=2,
                      sticky="NW"
                      )

        # Season Row (1)
        self.addLabel(text="Season",
                      row=1,
                      column=0,
                      sticky="NW"
                      )
        self.season = self.addCombobox \
            (row = 1,
             column = 1,
             text=SEASONS[len(SEASONS)-1],
             values=SEASONS
             )

        # Button Row (2)
        self.addButton(text = "Lookup Season Information",
                       row = 2,
                       column = 0,
                       columnspan = 2,
                       command = self.lookup_info
                       )

        self.result_fields = self.add_result_fields(RESULT_FIELDS,3)

    def fill_results(self, season_data):
        """
        Given the data, fill in the page.
        :param season_data: Data to populate the screen with
        """
        self.result_fields[0].setValue( season_data.league_name )
        self.result_fields[1].setValue( season_data.year )
        self.result_fields[2].setValue( season_data.team_name )
        self.result_fields[3].setValue( season_data.wins )
        self.result_fields[4].setValue( season_data.losses )
        self.result_fields[5].setValue( season_data.win_percentage )
        self.result_fields[6].setValue( season_data.playoff_results )
        self.result_fields[7].setValue( season_data.coach_name )
        self.result_fields[8].setValue( season_data.best_player )

    # Methods to handle user events.
    def lookup_info(self):
        """
        Read the year and team from the form, send a request to the information
        server, wait for the response, and then populate the results form with
        the supplied data.
        """
        request = Request(self.team.getText(),self.season.getText())
        socket = establish_connection_to_server()
        send_request( socket, request )
        season_data = get_response( socket )

        self.fill_results( season_data )
        socket.close()

def main():
    """ Instantiate window and start gui loop. """
    NbaRecordClientGui().mainloop()

if __name__ == "__main__":
    main()                                                                                                                                                                                                        data-dir/                                                                                           0000775 0001750 0001750 00000000000 14341774512 011163  5                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   data-dir/pelicans.csv                                                                               0000664 0001750 0001750 00000003432 14341765010 013471  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   Year,League,Team Name,Wins,Losses,Win Percentage,Playoffs Results,Coach(es) ,Top Player
2022-23,NBA,New Orleans Pelicans,12,8,.600,,W. Green (12-8),Z. Williamson
2021-22,NBA,New Orleans Pelicans,36,46,.439,Lost W. Conf. 1st Rnd.,W. Green (36-46),J. Valančiūnas
2020-21,NBA,New Orleans Pelicans,31,41,.431,,S. Van Gundy (31-41),Z. Williamson
2019-20,NBA,New Orleans Pelicans,30,42,.417,,A. Gentry (30-42),B. Ingram
2018-19,NBA,New Orleans Pelicans,33,49,.402,,A. Gentry (33-49),A. Davis
2017-18,NBA,New Orleans Pelicans,48,34,.585,Lost W. Conf. Semis,A. Gentry (48-34),A. Davis
2016-17,NBA,New Orleans Pelicans,34,48,.415,,A. Gentry (34-48),A. Davis
2015-16,NBA,New Orleans Pelicans,30,52,.366,,A. Gentry (30-52),A. Davis
2014-15,NBA,New Orleans Pelicans,45,37,.549,Lost W. Conf. 1st Rnd.,M. Williams (45-37),A. Davis
2013-14,NBA,New Orleans Pelicans,34,48,.415,,M. Williams (34-48),A. Davis
2012-13,NBA,New Orleans Hornets,27,55,.329,,M. Williams (27-55),R. Anderson
2011-12,NBA,New Orleans Hornets,21,45,.318,,M. Williams (21-45),J. Jack
2010-11,NBA,New Orleans Hornets,46,36,.561,Lost W. Conf. 1st Rnd.,M. Williams (46-36),C. Paul
2009-10,NBA,New Orleans Hornets,37,45,.451,,B. Scott (3-6)-J. Bower (34-39),D. West
2008-09,NBA,New Orleans Hornets,49,33,.598,Lost W. Conf. 1st Rnd.,B. Scott (49-33),C. Paul
2007-08,NBA,New Orleans Hornets,56,26,.683,Lost W. Conf. Semis,B. Scott (56-26),C. Paul
2006-07,NBA,New Orleans/Oklahoma City Hornets,39,43,.476,,B. Scott (39-43),C. Paul
2005-06,NBA,New Orleans/Oklahoma City Hornets,38,44,.463,,B. Scott (38-44),C. Paul
2004-05,NBA,New Orleans Hornets,18,64,.220,,B. Scott (18-64),P. Brown
2003-04,NBA,New Orleans Hornets,41,41,.500,Lost E. Conf. 1st Rnd.,T. Floyd (41-41),P. Brown
2002-03,NBA,New Orleans Hornets,47,35,.573,Lost E. Conf. 1st Rnd.,P. Silas (47-35),P. Brown
                                                                                                                                                                                                                                      data-dir/lakers.csv                                                                                 0000664 0001750 0001750 00000014713 14341764531 013167  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   Season,League,Team,W,L,Win %,Playoff Result,Coach(es),Top Player
1947-48,NBL,Minneapolis Lakers,43,17,.717,Won Finals,???,George Mikan
1948-49,BAA,Minneapolis Lakers,44,16,.733,Won Finals,J. Kundla (44-16),G. Mikan
1949-50,NBA,Minneapolis Lakers,51,17,.750,Won Finals,J. Kundla (51-17),G. Mikan
1950-51,NBA,Minneapolis Lakers,44,24,.647,Lost W. Div. Finals,J. Kundla (44-24),G. Mikan
1951-52,NBA,Minneapolis Lakers,40,26,.606,Won Finals,J. Kundla (40-26),G. Mikan
1952-53,NBA,Minneapolis Lakers,48,22,.686,Won Finals,J. Kundla (48-22),G. Mikan
1953-54,NBA,Minneapolis Lakers,46,26,.639,Won Finals,J. Kundla (46-26),G. Mikan
1954-55,NBA,Minneapolis Lakers,40,32,.556,Lost W. Div. Finals,J. Kundla (40-32),V. Mikkelsen
1955-56,NBA,Minneapolis Lakers,33,39,.458,Lost W. Div. Semis,J. Kundla (33-39),C. Lovellette
1956-57,NBA,Minneapolis Lakers,34,38,.472,Lost W. Div. Finals,J. Kundla (34-38),C. Lovellette
1957-58,NBA,Minneapolis Lakers,19,53,.264,4,,G. Mikan (9-30)-J. Kundla (10-23),V. Mikkelsen
1958-59,NBA,Minneapolis Lakers,33,39,.458,Lost Finals,J. Kundla (33-39),E. Baylor
1959-60,NBA,Minneapolis Lakers,25,50,.333,Lost W. Div. Finals,J. Castellani (11-25)-J. Pollard (14-25),E. Baylor
1960-61,NBA,Los Angeles Lakers,36,43,.456,Lost W. Div. Finals,F. Schaus (36-43),E. Baylor
1961-62,NBA,Los Angeles Lakers,54,26,.675,Lost Finals,F. Schaus (54-26),J. West
1962-63,NBA,Los Angeles Lakers,53,27,.663,Lost Finals,F. Schaus (53-27),E. Baylor
1963-64,NBA,Los Angeles Lakers,42,38,.525,Lost W. Div. Semis,F. Schaus (42-38),J. West
1964-65,NBA,Los Angeles Lakers,49,31,.613,Lost Finals,F. Schaus (49-31),J. West
1965-66,NBA,Los Angeles Lakers,45,35,.563,Lost Finals,F. Schaus (45-35),J. West
1966-67,NBA,Los Angeles Lakers,36,45,.444,Lost W. Div. Semis,F. Schaus (36-45),J. West
1967-68,NBA,Los Angeles Lakers,52,30,.634,Lost Finals,B. van Breda Kolff (52-30),J. West
1968-69,NBA,Los Angeles Lakers,55,27,.671,Lost Finals,B. van Breda Kolff (55-27),W. Chamberlain
1969-70,NBA,Los Angeles Lakers,46,36,.561,Lost Finals,J. Mullaney (46-36),J. West
1970-71,NBA,Los Angeles Lakers,48,34,.585,Lost W. Conf. Finals,J. Mullaney (48-34),J. West
1971-72,NBA,Los Angeles Lakers,69,13,.841,Won Finals,B. Sharman (69-13),W. Chamberlain
1972-73,NBA,Los Angeles Lakers,60,22,.732,Lost Finals,B. Sharman (60-22),W. Chamberlain
1973-74,NBA,Los Angeles Lakers,47,35,.573,Lost W. Conf. Semis,B. Sharman (47-35),H. Hairston
1974-75,NBA,Los Angeles Lakers,30,52,.366,,B. Sharman (30-52),H. Hairston
1975-76,NBA,Los Angeles Lakers,40,42,.488,,B. Sharman (40-42),K. Abdul-Jabbar
1976-77,NBA,Los Angeles Lakers,53,29,.646,Lost W. Conf. Finals,J. West (53-29),K. Abdul-Jabbar
1977-78,NBA,Los Angeles Lakers,45,37,.549,Lost W. Conf. 1st Rnd.,J. West (45-37),K. Abdul-Jabbar
1978-79,NBA,Los Angeles Lakers,47,35,.573,Lost W. Conf. Semis,J. West (47-35),K. Abdul-Jabbar
1979-80,NBA,Los Angeles Lakers,60,22,.732,Won Finals,J. McKinney (10-4)-P. Westhead (50-18),K. Abdul-Jabbar
1980-81,NBA,Los Angeles Lakers,54,28,.659,Lost W. Conf. 1st Rnd.,P. Westhead (54-28),K. Abdul-Jabbar
1981-82,NBA,Los Angeles Lakers,57,25,.695,Won Finals,P. Westhead (7-4)-P. Riley (50-21),M. Johnson
1982-83,NBA,Los Angeles Lakers,58,24,.707,Lost Finals,P. Riley (58-24),M. Johnson
1983-84,NBA,Los Angeles Lakers,54,28,.659,Lost Finals,P. Riley (54-28),M. Johnson
1984-85,NBA,Los Angeles Lakers,62,20,.756,Won Finals,P. Riley (62-20),M. Johnson
1985-86,NBA,Los Angeles Lakers,62,20,.756,Lost W. Conf. Finals,P. Riley (62-20),M. Johnson
1986-87,NBA,Los Angeles Lakers,65,17,.793,Won Finals,P. Riley (65-17),M. Johnson
1987-88,NBA,Los Angeles Lakers,62,20,.756,Won Finals,P. Riley (62-20),M. Johnson
1988-89,NBA,Los Angeles Lakers,57,25,.695,Lost Finals,P. Riley (57-25),M. Johnson
1989-90,NBA,Los Angeles Lakers,63,19,.768,Lost W. Conf. Semis,P. Riley (63-19),M. Johnson
1990-91,NBA,Los Angeles Lakers,58,24,.707,Lost Finals,M. Dunleavy (58-24),M. Johnson
1991-92,NBA,Los Angeles Lakers,43,39,.524,Lost W. Conf. 1st Rnd.,M. Dunleavy (43-39),A. Green
1992-93,NBA,Los Angeles Lakers,39,43,.476,Lost W. Conf. 1st Rnd.,R. Pfund (39-43),A. Green
1993-94,NBA,Los Angeles Lakers,33,49,.402,,R. Pfund (27-37)-B. Bertka (1-1)-M. Johnson (5-11),V. Divac
1994-95,NBA,Los Angeles Lakers,48,34,.585,Lost W. Conf. Semis,D. Harris (48-34),V. Divac
1995-96,NBA,Los Angeles Lakers,53,29,.646,Lost W. Conf. 1st Rnd.,D. Harris (53-29),C. Ceballos
1996-97,NBA,Los Angeles Lakers,56,26,.683,Lost W. Conf. Semis,D. Harris (56-26),E. Jones
1997-98,NBA,Los Angeles Lakers,61,21,.744,Lost W. Conf. Finals,D. Harris (61-21),S. O'Neal
1998-99,NBA,Los Angeles Lakers,31,19,.620,Lost W. Conf. Semis,D. Harris (6-6)-B. Bertka (1-0)-K. Rambis (24-13),S. O'Neal
1999-00,NBA,Los Angeles Lakers,67,15,.817,Won Finals,P. Jackson (67-15),S. O'Neal
2000-01,NBA,Los Angeles Lakers,56,26,.683,Won Finals,P. Jackson (56-26),S. O'Neal
2001-02,NBA,Los Angeles Lakers,58,24,.707,Won Finals,P. Jackson (58-24),S. O'Neal
2002-03,NBA,Los Angeles Lakers,50,32,.610,Lost W. Conf. Semis,P. Jackson (50-32),K. Bryant
2003-04,NBA,Los Angeles Lakers,56,26,.683,Lost Finals,P. Jackson (56-26),K. Bryant
2004-05,NBA,Los Angeles Lakers,34,48,.415,,R. Tomjanovich (24-19)-F. Hamblen (10-29),K. Bryant
2005-06,NBA,Los Angeles Lakers,45,37,.549,Lost W. Conf. 1st Rnd.,P. Jackson (45-37),K. Bryant
2006-07,NBA,Los Angeles Lakers,42,40,.512,Lost W. Conf. 1st Rnd.,P. Jackson (42-40),K. Bryant
2007-08,NBA,Los Angeles Lakers,57,25,.695,Lost Finals,P. Jackson (57-25),K. Bryant
2008-09,NBA,Los Angeles Lakers,65,17,.793,Won Finals,P. Jackson (65-17),P. Gasol
2009-10,NBA,Los Angeles Lakers,57,25,.695,Won Finals,P. Jackson (57-25),P. Gasol
2010-11,NBA,Los Angeles Lakers,57,25,.695,Lost W. Conf. Semis,P. Jackson (57-25),P. Gasol
2011-12,NBA,Los Angeles Lakers,41,25,.621,Lost W. Conf. Semis,M. Brown (41-25),P. Gasol
2012-13,NBA,Los Angeles Lakers,45,37,.549,Lost W. Conf. 1st Rnd.,M. Brown (1-4)-B. Bickerstaff (4-1)-M. D'Antoni (40-32),K. Bryant
2013-14,NBA,Los Angeles Lakers,27,55,.329,,M. D'Antoni (27-55),J. Meeks
2014-15,NBA,Los Angeles Lakers,21,61,.256,,B. Scott (21-61),E. Davis
2015-16,NBA,Los Angeles Lakers,17,65,.207,,B. Scott (17-65),L. Williams
2016-17,NBA,Los Angeles Lakers,26,56,.317,,L. Walton (26-56),L. Williams
2017-18,NBA,Los Angeles Lakers,35,47,.427,,L. Walton (35-47),J. Randle
2018-19,NBA,Los Angeles Lakers,37,45,.451,,L. Walton (37-45),L. James
2019-20,NBA,Los Angeles Lakers,52,19,.732,Won Finals,F. Vogel (52-19),A. Davis
2020-21,NBA,Los Angeles Lakers,42,30,.583,Lost W. Conf. 1st Rnd.,F. Vogel (42-30),M. Harrell
2021-22,NBA,Los Angeles Lakers,33,49,.402,,F. Vogel (33-49),L. James
                                                     data-dir/bad-file-name                                                                              0000664 0001750 0001750 00000000000 14341766064 013460  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   documents/                                                                                          0000775 0001750 0001750 00000000000 14342161050 011463  5                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   documents/use-case-document.docx                                                                    0000664 0001750 0001750 00000777110 14342161042 015701  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   PK  o��U               _rels/.rels���J1�{�b�{w�UDd���ЛH}�����LH�Z��P
�PV�3���#����z�������a� �u����M�h_h��D��b��N�
F�����H^�#�r�s�Z�1�y��i�0��n�Ym����+�v���׍�D[-'Z�T��8ʥ\��D�e�\����K3�e��� �{g���S�K.:
Kv��c��\SdY���D������i����ɢ=�ϚE����}PK�r�D�   �  PK  o��U               docProps/core.xml�R]O�0}�W��C[X�`��=��d[4��rǪP��ۿ��`S��v�=��~5���ۃ6��)�AH^�B)Z����e2ge-!EG0h��$\ż��k�
0�3�&�*E[kU���[��	�B:rS�Yu��_� 2�X�3�pk���,s>Z��.;��c(�i��g�]��:�BY	{TpU:���`�(l�&h�N����m��F��lW�eɩ��k`r��}��y��Vs��$}J|z��Ә�Ǔ�{��o���Y˞��s0\e�{�G���b������N2��S��؅;�F@�ptWrCG�)��H�O�ܷ#E�b�����a/ڿ�E]��]���'pۏ4[aK��C��?f�PKX"g  �  PK  o��U               docProps/app.xml��Io�0����ŕ8�E�Q��T���[�:C�*�-� ��5DMs�O�捿�l.]��X�d��0BH�*!�}��%
�c�b����+X��dg������Q�^cly����w��t�yij��G��E�S��$�2��j� ���/�R�v>�/���()��-s@	�+�X[�h���A�G�[���OB�����=/�4\��d+��R~.�2��������i4y:���&�a7�k��ȯ��o��X���rP��4YzN_��Ɲ�@�t� x���w͸���<��,�gXm�n|HzK�Ç�PK ԇW8  &  PK  o��U               docProps/custom.xml�α
�0��ݧ��T�Ҵ�8;T��޶so�M�}{#�>N�=�C��j�/+) -'-o��8I���`���,�v�\#���, k9�j�����9c.#EoR�qR4�����:T�Qم�"|9���5�Kd����o!{m�~g�PK�� ��   �   PK  o��U               word/_rels/document.xml.rels��͎�0�OAz�*��b6�a��P��i�f}�m�QL�f���̯=�)�?|��A&E��8A�VvL�
}6����E�#�n��2�;#L�k�Ʀ�K�}��ĺ��X���P�Y��XO{���gt�*��]����?�e߳�=s��l�e�:M�V躎]�_���ϸ��c:���k1���Va�ϰcX��0��ϐ�1l|�mC�3a[�a�P�i2'B��	�K��^�T:kJ�R؆���s�K^Ŭai�Zw�iZ�*7â�O?��PKc���  �  PK  o��U               word/document.xml�]Ks�8��@�S5�޲���r;і_kə�S
"Ac� �d�)c�v����K�|H��cٱd�`������|��:�Ȅ)ͥحԷj'}.ƻ���ѫn�hC�O#)�ne�t����^O{��Ҙ	C���=�[I��i/d1կb�)�e`^y2�� �����ڭ��$�j5o�%&�^ UL\�q5k�.V�Q�u��E� ^�D�&�=GE��]�:��O���� �8ʞS.J2��F:e��.O��.<rȻ�朢�A���0r�Y*@�^��� �	�S�F���iRP���pSu�&(�zt�#nf��9�zk5T_��~��O��c%�����B*:�@� 	A�P��B��?�cbΕ=�,bdڛ�h�r���*U[���(�eE�{E���TV�2J���c5�W-��n�_�9홽��!9؇�wg�'��C�k�:��!b�Y��6�����p��tB=i�b��	��C�Ii��|���+�9%��$ՌȀ������U��M�g&��K�����\��.5������h�NG17��d4#�`A@��+ ��F��_�����eb�w�B�b8KHn�oJ�T�#\h�R�
 :Ŭ~̵b�MH.G�0)9�"�.�&�hl�Z[��T�A�b:##FCyS5#< 3�Z���,
ZLa?T ƪ£���B���-~I��-/5����J^r������~��~0<<'��/�d���O��.N����S28��xx�ą%(���vm�8�lL�Pc~>�Q$1:�D���P,� F�"Fb���-�f�Bj�� ���Ȣ:Ǌ��2m���@�l�8�S�qV�G��+�p��e�|8�~Z� ��Q�(�B�ܙ��8^��F�4$���iң��4�Xυ�(>,�6���myv\�]�3��$b�R۫HzW��N)8� Z[`5�,�	v<�&����q�6*NI�\�v��礗H�Q?�m���aB �4Ys��˦�pQ`O��K�>~E-���M�JQ�,43{�f� ��,Q�h��k�~��z�����F�Y�u
N �@�0�����_eGs���d�G��O�@��*p�&�!�"ܷR4�qޏ���ϴ$+R[�6�N'�E�)h���7^(9�������cj�e�̢�}� ������U��@�5���߃T�=�*0�ᬗ���lejbr�mO����W֜7�HPD���Miϋ��ӐQ_��L�z�(��8A|��c��[�}T�jV��!�d��4�&����Pި.��+扌�'��ij����@�x�0)Z���u�^U����{&c�' Y�tr�slE��NJ9����0����YMkSKc�L]剜0��0F����~��ӬY��'h$��)�����
�ha��k(N��Xe����~����v��ݮ�e���i��m7�ù�r۷��z��擺�凞���#eE{)����ȓi�NeēqL��[G�Y�u�{��H
�y.�=��H1v"��d��^,�˔�=�� ���2�y޹�͍fZ�-��4��Fav���Fw�Ù�Cl�pf��zo���f!��W.�Y9�9�we�&1P�����`���=)�W2��&/������$�E�1�"��p�L$��.Q�tN=\��(�e���`%y��
Ϟ�b=����삜_����=2��+L'�B�G��q��dP�K9v �F	����!���P4KEM�&��q�)24��<��|�1�S�a!�	��ۥr�Lc�HRܞh�����u���+�b���x:,���0R�UL�͹�1�= `�L�`aNu��O��I܊�N�)��/��LŸ�w����p�g��}]��܀���2�A4�0��}K�m��v�R��8���Х!�$�0������o'%���#�4N�jو�q�$�G��:&9���g �n�V�--�K7��6y�Eki��rɎ�Jv��{��h���͂^=�d�O���%S���Cg
��Fk�s����4yٷSQPo�X������J��t��F;S�f���y콊�%��v�s��m��^����{z�����sLe;�O�'Ǔ����xr<9�O�'Ǔ����xr<9�~"Ok����#��1\�����ۓ��\���p0$Gg�ob�֏���|�e��"�@E�a4�vG��A�·E3��F]m+�N�ӷ�d4�G������`s
E�g4�d$�xS嚨�C����ss��w �:����lj�t-�Y�ujŚK���>�?pw�V�:n-s��2o��Z��~ڵ����F�e�t��9d�C�9d�C�9d/�FeG5�?ePd7ٵ�dB|9��\�?)_rF�����;�oy�t�����.8y�4��R"eۥ�6*v[�W���i���K�����!s�2��!s�2��!s�����;WLg�{��HA":b���K��J�"Uן����?WH�m�X>r�}kăo��w�Q�<�N":�/����|��6M��!���1]������V�Y����mo?�{�K	׮K�oT����[�t�����^�t��"��!s�2��!s�2��!{d��k;���B��-Ǌ�ѓ\x�g�c����1�bJ�)~��E=�q���
a�e��3F�!��*�k�e@����7���k��t���{χ����xr<9�O�'Ǔ����xr<9�O����I3�d5�,)��ڜ�1�H'���r�[�7��+^�U�n�VT8���F�7[XGe{���qj���@{F����d^-�r^m$��}<�f���4fP������q�ƹ���#��Ι0��;�u^�]X�OG�m_z�Ga��l@�� ��v΍ڏ�a�R5H���Xȱ����=�ī��?PKP��4  k�  PK  o��U               word/media/image1.png�ywTS�����A�
���޻H�� HMz1��" ��Ћ���:����P��й���Y�u������w����;3ϓ�>|�����   ��}- �Ā���_M���QWK�,8c�@��l>��y�1v��W����j>��/ F
ޘ��7y��J��P���Z�����ܸ�B{�!�� oު�گ���O�]B����$$;;�G��Fɝݝ��8÷��z��8�^����k����7�4 ���6�<V�3D	 ��1�F���x��s� ͂�������(�@��W>p��ZA$��J�����֭q�Z7/0��Q� ̸�i�tX ll�K���&�U�H}(�6�������t�c�N�v~�0�\��m�=���z�[ ��A$	**����Cޜ��BM
���B6�ç��D#k4��pH���TL<7��\,�ӭ��z�}#��w�L�ob��g)ՈԚ2R��o��KH{r�O�Qu��[J�f7�@x�:�'��+Cx_ĸJ�����,닚��ņ�����@ް�h*����;z2�����<��"u��,�t�}̆�����G�IjD��-)��
kO�Bȧ��d'��>#o�+��5[����3��^h_6�65��K�� f4U%�`s�V�������z�2��5�YY`^,�+i[�NI��X{�w���.Q��p"�6q��C��kC4P#���@����3?!��9Ws�H�E����&�@����wv�f�R��5o��L��L��ډ����9O���p���R��*75|Iȧ�DiW+s�%G��1���W�/�W;uΛ��������J𥳐�ܰ�	�R��u�(�C^r�bq��9C���t�=���6J�z+`��V�ϰ��c�A�9�ȶ�T-y��%s��[kU�����������f��Ou
�Տۆ�������(�v���mr}�*7�l풍J���i2�Ħ33m@�3�g�'Ot~�?������/ar@�,r{�0�G�c�s ���E��[0D(�Д{�x(^Pni�J�Q�<<�������ܓZz��\[��w�a:.���v�2�U��qx�|�Sim���u�����>�����hkS�����q��'��cL�F�gF-���"�������
Q��%T�;�E�1Ƣ
���cI���_�8W��j������	
�#��;���wv���}�汊s�c�X����bVv

�Ix��2KQ۰5��\LS��rQ��6�P�wsI�z��!(1%�^����M�4����Z�L�f������b���s�NK��ѯ�V����E�����|k�Nu�M�Y�}�6,lw�%`��GY?M����ŉa��7�}��3���؅��k6�R dG�xAِ���~���Te�]c��5�\4���g�>����)�m�"�T�4�l���-�K�a�C��1��������0���ޞ���Œ�2�+LkE�
k����E�*k^	�6y��`��reiPd���T.�?=�5��7�J�е8Ae��x���d�t4'c����X2 ?�G�?ϑ�/]�������E���(���Џ�)���9��,�ۮ{Odq��:����i�Z��?g�?.��S�4h�ĥI�ZX���*k��q��-,�Q4 n�_�s��ֈ��j?�Gќc]�'��m}�hҔ�9�d��"J�Y*��8-�D/|�;\�8���j���O����7%�O���v�
C*��Qل�בRrk*vMz�i�W�m�-�ͫ�Ö(�Ȁ��|��vi�t�2�@�ϭ��p��'q(�e����u�7ň�:��..�Ҿ��t�]�Yν��t�JL�e�E����i~���9��F���O��B�po��-Dː�b�cS��]�xڏ�������/�C���+�������:���䪩�]�������ዤ�t�~��y�1^�K:�V6��V*�vyT�+��6p��i_�)����M�g�nJj�xN�P�!Ǉi�W���Eb�]ޫ^B�`O���d)��۸��4|���c�yy�&h���� ��?�Ph�D��1j)�^75�j8W�u���)���ғQ'��ݣh��o������|���2���]�%42�Ƈz���f5��0,��v�OP<�F��t�S�Bi��+�ו�.O!؉�b����_������iY�M~��L��H�	Ԁ~�r�\/VP�3?�^@�ʓ3 �E�V@l��0��*V�h?�-.;ת�%��L����C��%9d<�z".�xM�f�	Y� `-]��u�pB�D�����l� 6����10Ӟ�o�'���l��O����9���!k�R%�f�\��<*�"즇A� 4�(���R\X��R,=�`&�����<�i���N�y�8.u�&�cfR�Cxԣkhž��t�n�B�=�e�F��)�!��&��8��6x؝����	�R���o�!���z�Ko�*�W�C�i�W���`��B������7��~L��N����<�dy�։C"��r�����r�ot
7�67ak�_��#*li"���ZՋ��nrʬ�ʘ�Q�
Y�+�i9	�v�r�=��I:`�J����D�k_ّ��U-w6bc��7L
�6�B�cڂ��&wYfJ�v$�&_V��|*�R#q�Y�MFR�R�5����C����fgwVO��7��,ert�����VN"V����%%��u&ۙ����P��נq+q����KuP�R�<�"đƏ���|�z�,TL�Z���:���J���?bW�Qe*;����Ӿ��_%C'sl���Ҭ0��`�VH��Q���΢O�+�r)1"��.�+!+x�Bo7�Ä�N��ZC�4®�0"�ڼ������G�i������a#�A��
�`���D;3S.��Nt*V+�k֥�O�]����%ѓ��S|����/�DVq��D�2V�p�^�\�m�I8���3-z���T'z�Z�_h5�Qf1W��hr�F��i�����X?m�n�a[֓E��>���
D-�b*���˺�����}�&��%���G۽��,8d�����k78�@����-ć;CC({�L�$����_2�B*1\��������~}I//o�Y�}p*\�I��/�7D��l֑�CCܞN�����Y<�Dc@�[��]j[o�|ߎ����l�'�G��p�XCv���tY�[r��[O@ ?N=�ʹi��\�\Nhfع[��&�l����;̆��[�]��i.p�>�lQĮT�K���7m&T��}	�Z��@#�!`����v�wU�ܙ��S�]�Z~����S��1�rk�����3��e��Rh�����c�	Q�E������I��2o��Ec��(#�F��ϙw�M��B��k���M��e�=A�k��+Ǆ��1�ۋ�6�B|T��F��`�v��i�#��X�!���<���տD�Wi�cu�E-~���㑽W��|$��Kv��KC׸�iw�]�,�)N��,��*K�>���ixSHkx8cx����7f��ҨC[��މ��逵_-�B���L����]h�.�~tkqeI?H���x����9�?�	)�o^�lWВ��`L�K�1���Ģ���[��N�?57���v�C��D^���)��V�2T�3޴8���®��C��ev�Q����Wռ�N,ǫ;�xҹV6
�)��`�g03�li00�	*��1|��5R�x��`]�&�"?�#��v��ǃ`%hG����"vo�9ק���s`�l�:���~��Ft�Y�&OZ_ç��&>?��7���tMc\Gdh4�7D��K屮}͈z:�#�OA���TJ�8pq.���PR	A��<��p��ADC�kX�+�d~��N#I�/t�a�o�qB� jJ�H��!�K������`��Mv�D�o���4���)�]]?�l��7�X�	�KJJ~���"?��ۦn_ܶNqp)��L��y��m�TX(x���[-�������IoI����G�F���{��[]]�Cu4Rr�&!'�ޔ#k�B���W�\)E�1O� T����v���k�i����w�~X,
K�?��w��N�����sW_<B��͛�/4g�*++��( ����'L�R����H�l7�醋�}
k�X����9mT 3�wo���M���z�U������0�rk��s��5D�#���#�-��l��]`扖�����o���x�#�:+G��{��<��N���m�ʰ��u�ܔ ���pdm�����j�Dᖑ�w�ڇ���&����(#_jQ� ���xy;�328�\\���mU���*F䪐��Z�7`�6�c'UK+*,CB����ɇ�û�̀+3�Q128Nk��9�0�FVh�ø�f��a�	duFf�K��Ir(y�E[�B�`�0��^�2g��y��c.Zt{M��֯�F@S;Ū0����E$)x�v��H�9Pyg��Ċm'���7

�����q�׏�O쮕���NBJ)��� ��NB��s
��󂌰0bs���3|C�(�*<�ar	.�~д[t(4M�X�y_��ֻ�jݗ�����Q� ��
����=0��g�}�K�暩#G�l.�����c/c�x�W�M�����
Yu�����#SL8>I�Rۋ�# 9��8ϐ)��H�`65�(]-5_������%�؟4lI|qN�o�G����h�a��<�B�q���C,��_5

!∏�T	�(�\PRYmT���?�"{^Ӏ��'�~J/h��2�Ԑ�zN_��P�8y�*_'_l�_�-�~cV537�Hj�J��:! 9ʠ��-���]_���NNN�k�)�)�+,,K��u���4�uvvvY"-G��'��*��/���;0��^+u��V+��1p��k��6bz��;��/�V�_X꼕]�	 t���%g}�C1��F������X/��ƍ�$�
����	���k��*�iI�[?��q�a�>�`��E����6��h��p��Bfz^+���!�U���ǘ�0%�@	p��!��PW��g��� ?1���=M~�����z���8u�}%��^�D}�j��α#a��mp׆�������<&(*�Ր�Mu`�ڞ��+c>���]�L�ϯJ�c��+ml�票��h�>J��D`���Lb,�����~H��\��M	�i�[�&���n�l!����:x�A�V��_��\l1M_�C�k�����xf����&Z�{��������@,\i��U'�u�Y�G8���S���]�ٗY�È�<�p�<���l�����F��k[��`m���1�ڥoH�&|ww�ț�3�El��T�[�� �1�|�Z��e,�vꦶ�6w�O�M�#��a����5M ����'��]dxu�2�X�'p���tR5"h�w��� ����I��Sr|��/g���:-�t��S�.&�瑍v����&J�@��f���b�(���wb �<��ޅ,���pw/%h����Lh�@��\������ ��
�X���T �����������u ���@kZZJX^~l}V.��g�	���It�q��u�-�̊�����7�>�:9�7[C�a�
�>vo+X	ߵ �QUY�����t�F�����0��
��B� -��1�}�n|����ܱT�z,U�����߁Hw]M~ܠo�%���|BZO��A�J��O����
}�<�����T+���J��˴��p���Yw;�6�#1�V�Ļ�Iǘ@�'נ����I����B~]Kw[@���\f�󬍱%�IVU,tw��s�c�����6'L\�d
��uw��.��ө�w��K�7�����:�
p��_�X���ܧ�d��۹C��+i�Q����<���=��F]�G$ICx����jD�A�ֻGO�8����R;}d��2��7l}���(Q�&81�{�
�f.�਌*����:s�i�W���ͨ��������U-���1/XB��{�y��Qe���vg�.vt��vI���:�4q���~#n��w�k�&�D�GQ~ǥ�G�Si�/��9�n_g#��w0��f-빉����x6h�}��ƌ���l�M��o�W�%��~��?)�x�����J��&h��I-��˥WK/\���MA<�G�5�J�Lem�fM����,�KDnI(��{��W��ng/w�cZ�@Ǚ������-��;6�2*�ؕ��
Of7p�8�}TΙ�<�8�(��w�/q(ҳeX�^P�Vðq�mX'CyѺ��%j+�8)|뛍?��q����Ɠ�;O�P,R��  -䙂���zݍ����KٜSʪ�EC_y����˳=�T�+��z�3؆Ԣ/�T�~o�֕�>�^��a�g|��9�2,��x����=��}���f~�������L�=��Y�9��������DL�X��k6~���3��q��5y���}�13��7&sW��U.�&*1x���Ǟn��d�NeLG�n
È��_����o��+)��h�b�`9	�c�F5�|?�F����"Wͽ��=�,W�<CJ)�nɲ���x���x��ⷌ!]��P����Ѡ��,{���ٍ"������>?i�`k�X��0���� �w4iTx���짜�{y�vH�[T3:��l�K�6Mm�4Ϩ+��||M����5�
�~,p��(���d�/�>���2�̫ډ�Ki����'<8��p���L���:�,�©;�tg��ECr,Y�S%����*h[=QƞQT��e���/!����ú�<E�w#^���gӟ߸WHDg��m) �{�����O��zmՊzăF;Y�T~�5�5���P��{��R�vǮ���կu?	9
(�.�Ae�z�����V:�D��>��ZK/��ȸYtf�QpL�?""VmO<C7UIql���^I�|լU�[�<8a���Ԗϸ��]\V?{�F7d�O�mȥ�Y[�{U��e�䕞}��xJ!<�R��_! ?��w�w��t��5�}�&��6��d�dF
 A�L41���^Sfv�4����������ر``�f߷~P38RG�-�T����lJ_�8Ə�Ax/�Q�ѝ�/��Z».)���'�E���_�����+FFF=]�/aW���5Ð֦L6����[�e�S�SA��Y��g�[��l���w�*�P�b���e�����X,//�ʴ������?��j����gyҋ���\I��i���-a]]]�ӻ<��t���fyŁXp<^zimccl����������`�� e����FtuvPS�	O�|�+/&YM-�r|����'�(�W�cKˢ�R�N��Z#>�YX�+Fvgt�o�$�.�f� se7�\N���s�������g�%)S�S�H�{���)�����X�i�;�_^W��V�����PK�}�f  F   PK  o��U               word/media/image2.png�zUT�K.��5	���]���6k���n�=wN���ww��̚�3��>ޗZ�������v��vE|U�AC&F���B���T���[��{����Ј
*�ENRL�u�� ��Њp�>v��Χ�U?����h�D/������:>��+�m���"nc�8	����Z�{c-��ڃ@�$���u}�$ ;����D��)}����Paa�M�QuXS���+�o� ^^E�]C��
"U0�����#3Y�teMW��瀤��f����×�k'���rS�nt,,��&lg�)�Mg���������qd�ï'�1$��$`1`#�o2!$�����t�H���LcC*��BQ�R��8�&$�]����+�?�� ��w�T��X��o��i��+ՇFw�z�p���1����a�_� �G$�@#:�	�_�2��0p�%����.���Dx�g��w���l����O'���������S�����W8]��#?�Ax�2������-�E��eA��|��U')�]���S�?Vސ��� <l�����J�K�;ɘ��Y��������ԟ� c�\�
f������-^�}Vލ�:��Qq$�R���AzT�,�Α�&�4���ή��Ưz.��,�U��C�ku�lj�1����l6^X����� �%�Ƽ�7^�`�,�G)��/Pz�0�����C��	c���F���d���?��&�O��H�b9?"���q�k.��I�94� �V��LL8��qoڍ���|�ؾ_��>�0��0�<�zk7�5���(�d���Ra~/��F=l�U��C4�!�l/��*7��/��/��\H��3�v�'�y���8$/�-�����_{��%�.y�����J���X]�P��C��C9�Z�kx���U�ҵܿ�-0t�یQ��n�[��ɔ��̄�b�,)�ڴn^=�?���Ԩ(uq���c��'R#.o��ä�x�����@�r�J��DP�kxS�����$R]]}���+���R��z~�Q��p�]�9&�Uv�Z����_�y� ��\ ���N))��tc�T�U���>T6w(� ]IwC����Pm\��P߲�rC!���;����k��6u[�>���Wv`�:Wa���b��.L�+a�NF��$��c�< �'1*���I���p��sg�J�bt=VJ�~���/�]�6cdJ �p�N�nO�[R[xܽ���aaX=$����c�(�[I��������E�xX$�E�o�`��������1b��f\�B�w�o,�&�9�6�.s�	����Z���!mp ڇ�G�ʈ�g�<wR�]��oY��g�rgQ�������O�UA�ד�ɬb�����T�����k\��v~X5F_�9��7�F<\���{o��J�N��b��6���W�'�~�zHo��J�_�慘�N흍�0�^k'��b��)�7/k(�&��N�6}o)��P0�&_�w�AH��������f��e�=#�DD)4dk��"(r�1#3��rz#od�u�bw�7�T�F+R�g�4�i�n*R+���m���F,�K����m���9rbt���&z ��<@;��&7;�ܛ�D�Wg'�����J��jg*�~r=s`b?��/7����EE�L�|(���GmA=�SiR���G�����i 
���94��`}զ�N{��Z�m�f�	g���	>&6�r����qOܘ��pt-\��?�t��JY����8��RC<��hs� �y���=9L�,Vy+���u!Ǎ�0$_�:a��L^��5�VC�R��u�����u�G��𖴂�/h���.Y��P% 1�׿�l�.�u�Q������O���%^�����5���$j���!�6q���v��>��E�7F��~��1 ����4�b��/G�k[��ٷO5���n/z��O;+�b�J�p-F�R�m`,z�e`��p�V�;����n�&\�D��x��x<!���R.���ݙU����Yپ%G��1'�w��{?�`y˕�Cm�2��0D������3GI5Ȼ/LL�͗C��$0J�l�b~!�aß�XYCN�'ׇ��(| ��_@4�=����B�L���'sM���6�o���q5�jh�E��F��.�ӡ(*v���d�/�Ƽ�K��1��RFs�����{kRv^Z� ��&��R�p-���y%�n���Oe��ބ�.+r�氭�a<9_Ks4�9��������>؂ ������y�!U���E�[����z���r�nmZ�}���Y�a˜^5�f�>m�L'i�%m�t�����\�$nW���[U�g��t�E�+��V�0D-�s�Q�34�B���{r��:����q?I�m/a\q�ss�Zq.?�}G����J�)�u|�Y|���>(ieU`n�o���Ǭ��A��ї[�Cgם$��6��H��ο�
�rtt��1�t�?G�2Y�O�t���TV�������'��MI�㣭�i�L�>+�^�H�L�8KV�������$\�l?Q���i�Z��U����YH"��4�m�|�����"-��E���.���Cv�5j�����O��I�G��������<��z��Ѫ����̰4(ι���f05����أ���9�#v��XID�Zg�l��~咵G�P�m�El.�~�����5�H��&7��̕�i������.�p�cG���wB��MU�6 G � ������8�
����M�(�o0�,�"�	���S�	}u�Q8߻�FT/H�PO��۽�p!`�;�����j��}����4��@�Pp+�t��X���1��zBf@׶�r��G2NJ��h�%�0�j�~��.�(Ϊ���o�/�
�~�z"�A�P�Ԝzh�Y,Oh�f���/�������Z�$n<6E�U3Z1��E��2��6��b��AQy&#�N���Q��b�7Ha��(v����Rpm�6%P���i��Rj��Wn��_I��h���u�-����ʕL�:'}-.p�΄;GN\��S/�jY��K��m�j�p����o^�����ZH�F�HQ�����G������S�!���Z$�B'W7�j��cu՗�����fI�R�w�_�y&.�{A	�:n������[v��zRM�7P����v.����γ�;���M����S���S�?A�S&����2�����Δ��wL���῝�U�1��)S tz��+~�c�JUԨEWSH���ͭ��b��b���́b,:�Kh�
-���b>#�2�
CBzj&J��t���VIN�	����I�'}�NvpI��A�j�5Y��`�Vi�T����$BVٗ�O�W� S]�c�����ʄQ�1e��q����)R��V�i�C���jv"���G+�ȉ��� �"���f�#d�����罶_�b�Y�ܪ���7aj� ��k�������[��ָn��,���@I�<��q/6�r/W��R\N��P��/�����m�A}r��/?����!I�5'��#�*�	.�{Ϥyw��D2G7щ	E�_��{~H���,��Ӟ)iR	{�|�r�A�A
Y��4$j#Mq�ڑ�����.�������EnS		�"ǋ"�᳉�`��	3믺mTe���ɱXN�9kK�!�--��+'���s}�pxp���d@��t��`�*�_Sʢ]?��%�J�^;`Vl	����!�'�-��Kj����-vh>���H!$J��{��7�l��������X��+���3���@>FcO�D$u")���*QB�Vu�,ʴ����Z����/";sN�� ު!r�l]�ٹ�0�������O��\*�ߍ��D?�P�|��Rw,�b�r}�"�/�e�s�Hv߬����t�@�g���m���ծ����ߘ�m��(*7:��2l�t@��VD^�$�9��e����Kd@��V�pʀ�(�+`�e�M�4#�5��~ �P�TA�i�J�\q��t�l���Q�ֲdws��H�ۜo�[i�]G�h`Qn��� ��_8xd�R`��J����"w���X]����V��o�r�V��
/��1���?Z�����ؕ-��w��f�F���/��<"����^h~�U��
�i�U-h��r�gSD�7U���bF�\�z�e���ܷ-�f���*��Y��{ݶ4�]�
�Z�};~׋�2��h���WF�I"�����Ӱ;m4L�#���㗘��0갮'h���N����Y�g��y�b�%��Gg[��eJ�L#�g���Y̵&�з�c�{֟�I5˒���RIrF~1��,��U�k	��d����l��n��v�y1;>r��N/+�Y�E2�Vg��iX�H������7��p-K+�5�ړ���b�8qH"=^0�i�ЋEC�c�!�Մ�1�"#��)����S�O޵�)h���)�ޣ9(~�9��ݽ��N,[��#��G@��mg O)(:\���t�A4��"�=Y�ϭ�Ӣy�N��٣s�m�4��X;/�ǥ�d~EU���S�:��tk�Nj��|ؐ/}"K�ܕ�`5�K�i�4��[i��L$!{������X)�#�[\�h#k�h�}wMO#�DU�t�NϘ�a����Q����;#�u��C%����B5�_��L����f�=�P�~h����=��(v���|<�'uaI�ܣ�t^o2!��򏬀�Ǖ
�u�^*R��|��Һ2��	��a��@�;�>�?c������_w$Ұ�� |ò��A�#f�Ԝ���qY�X9\B�#�3�����ʁ�1��6V�Quv�`����z�F�$�Ϸn�(�?Ԩг"d��79������p����;I�ڌȘ�Ӥ��iA���!�.�x_�*������`T���K}�¦�/Ю���d�&&[D�Z��!ʤ�i�}��e_To�C5o��J�6�].���PkĒ.�@�k�X���ė\{c.�����w��O/#���1;�dY���C�;S�E�N�7�	��>�tD��L���g#n���ݶ��@H��I�t�	����2U�7a5�j�PFo��Y�6ؠW��\�|�ڨ緤��8��T-cu�]+8������E��{H� ���ke��&�?��-Xݛ	����?�d�s�d	o�4\�6�JH�q���:���S혙 k������N�ѧl4ɑv�F��%oe)�BV��kr��n��sH=���%}p�ɔ��{�p�V*�`w�')�ڌ�Ww��e_��'ur�P�qI��y�ة�΁�0;��c��Pt\�*�ЖQ�'Z��AI4&៲��",,�.�4�&, �a���z順ij��Y�}�[?��~N��p�����L,e)>�ٳ�9��r��ʎ�)�r"��1Gk�$�\��:�[A."�k���O(�؎y>�~��Ӄ�j���Yzwf�}��v�� tڣ��}�o�h��@5�,�����1v��-��6����w�mЅ�����ɋ���B���h���Xqo�M��*�d�Xd��hY����g9�C�b.���ݛO�ѐm����淃�ݱ��o8& zI�аG��޼��S��x�>�H���)�%C��3k���� ��uvM��/��L3��pj#�L���ڻ�zQ��`T�d��UI�ل0��&q���m�oᗧ�"1�Y軚�C,�߃�y ^�Q�xC��(
��:;&}�b�Q%e�q�^�	nVuh)>I�x)ڷR��L���
���e����g��c���y�m���?�;^��E8�L��7�w�77[��
a4=���H5FK�*��Bϝ;��Qb������|�8Y��W(�����6D�R�U�zaK�ܐ"��᠊�x��jn�
�#ҝZ��y��y`��2��:$�˭r��������jIr.R���x�L~����T�4�U�������u3�S�O�M~#`�ÎYB^+�Jё`r�����O���Q2� ��l���2qnt�h�}�ǱNyɬ�Mv��	z�T���Q����R%�	R��𿍃R<D�R���^|/D���^����b����_x����r�u�zjo��FG(����Є]iS�t���k�G�Z;ȯ�@ �@��϶v����P�<up�7=�z���K����:���W�(eh���VIo���}���b��y`���i�~V�|�T�\�5���4kID�G��B�͒d����;?��Ɯ��4MGX�	B���ɘ`�/|~��k��
� �1�Y��Ѱ��}��f����,m���y�@ A"�KI��SS�m0���]�.2F(�?���zp�Y>wǷ�e�˔�1�x�ێG�C�SD��닥Y��Rݯռhy�m�T~�"�*�}��Q���o�~�&tT��Ϛ`>��_�$V` �n�(�
g�1��,���~D���}r@���u���4�ċ�[�,o��U>��}��j>=��67["H���=AIߤ�g�JX1R^�p����#�j����m�ٯ�d��O�dOH�Xc�bgiKG]F��������&7bw/(�?)�\�C(�l���%L��m2nE0va�N2VW!1�1h�g���݋�?3���|�0���mȑ\�-{)�&?���r5������a���C?�/?X�
�V�����2hq�eSb��5�ى�\�]��25������Cs<����h��h������Tθ-ls�]���=�˚�mmþ���L������/������4K����8P��@yh���x��%@��*���m+�u�X�@z{�+H�K׶�n��0�b����{����n�b�����5�B'_�٩5dq�66����ae^�Z��qDD-l�";����u�s�hg��|���ۉ想�6�>NԴ�jd��_�>�U����[3:���:)I�>�Y�F�7W��u��ȓ���'�mz�C̶aJk���K�8�b�2&���(���XⲌ�	O\�b�a ���N�8+C%C�17���������{�c��g�rB��I���7�!�έ0��r���@�`�>ɻ��<,]�J�D���:��[��{A�����[Zۙ�6�Jb�'	�|x�d߭�Ȼ���B���MЄ��eu��m�Q5Jd?^�Y��a&��T�2sz��� 7eh���+ÚsG�z���n��]��$̓��.��0؛�y�8,��>�1��
ԡ�����;��_��z�3��Ά�:�ޭ�Hv{f���ˈ�|�7
yyb(�h�L.���h-�d#O.�q!�zғ�j�69)"��0n�O����3 =�<���dw�vj6��ÙpW�h��.���2kwk�7{�ng�����oc����d�e�G����ڏ��\��L'�+{�����Df����ٷ:J��xO��^[����3	`~�����߼|7�э@�"V㺡�e�|E-���������˯
d�A/K�s�����D��u �9�6���&�ӳ��߁#":�O��rtҬ˲F��t,H)b��M�(pW���
��"w4B�J_��㺚��{�$�:�_r�}{��&�^�s���I���W#\n˸N�/���^w�5�vc�&��|�`*��O�V��<ŝM,>ą�[x�V�^co����@#8�"��
�s��Sv��)7�e�P��dp�XeEK��R�M�R�������u��=X]�^nvݲO�q �n���񀫰@����/E�7D�J0� -'���`�Hw"�t��*�x�S����aw%2%na�e\7�Ȃ�;_�'O�:8a��H��a��HŤ��N�o(�(����l�mQ��L���:0�=]9C�>aݒ5��<5����DD���=j�>�_X;��B��"[����P�*kDh���^���%o��?RA!;�QXD��8t3��y%s/A2�7E�$��Rtc�5�i�8U'�b����{^@G	�����:q���jj�deS�����N�  �v��E���h���7,�'�7����7�i����iό��'��R��ŉ���ƃ�T�㢥��IO�φ�{-����ʄ�A1��fX� ��i��<`���+]�vЋl�vh�q숓%�Ii.��ʬ����[ �J�$�_���.��:� ��(Q�sw�c|�ă�3�*o.z̜�Ŋd���4��f���u0������-�y@)�D�ЊD)����5�	a��\#�`�V��䍒Ps��:�iB?QS�!�f�ՠd��!E�ˊkY�1���)�^����P��r�,��M����9�x�~|csj��m���M�,8��?'q�����ľg�C�2���K���a^�����z�Gy����V����J���[!T�q�1�("~Q����-�+��!�-MT����9Q����������i�|�R���[K;�lB�p�\�W��	~a�>�1�3a_/��<���?,��T��D�j0���RW�p��j��p��``�9@|��'={��>�92&&0��sBl�.��Q?3?���6�T�f	ar��,E���r}��Yy̦|��0�DC��`�FX+�ҹ�i|�Fd�%��L�`�$��5��P�CP�L>�ϣQl���s�������X��JYd�+�қ"eo?�<-�V��]�����@"b�Eo���ؐy�9_�G#��s�-x��ޗ��Y�v��.@��c�^���y{�~pwբW��M�OT��=ܺ�r���w�T����gnT��X��$DrIA(m�$FX��i&���W_�};H0H8q(p�~?�$�㝰�oi<�<��0���`ޜ��\}}(u��!��R9��?�T�˘܍����V�Ȣ�U��yH ���+�q_ ��~ߍ�*�w{]N�:/���0b��H��ɠf�uޛH�`�R���`��Έ��v��>��v��d��k�ھ�Q��^8�$����ڱ)6^��¬��p�[�9�c�{.��$Z9���A����G�f��ǀA%���#4�!��C��6rF�޷k���!��	.��b���w+~�;�A�։e��Lq�6ȯ�L|X
d��w����=�;^���6�o}��M�e脯G�����兺�m�!q,;dli�؎���e/�w�fϥ�f�x^���
\5IcE�,�Aꠡ�{�
�j����*F{��&2�oZ�'s��w�����k�������".P۽�	�#�a5����f��l����7)9���B5v4�(.��H�N���q;}ۉbn��"��c=�$��/.5��>-��X�~#�7��3�2�u���#��x��C&��N����D��>��2(�Լ��TB��w/F��Ő����{	il��� 	&�,T9�:.ȓ骯/������X���\G4���6`4RŪ��_��+R5p)�4�2k��)��so�k��g�����R	7yg
��N���4����Gc�jL�C��3^Ր��3���y� h�lq_���F�HIB<8�L���Y��r,CR�Y�2[Lm	������BgK�����l�W���/2| ��{���#BȪg�NHݶ|	�>ϯ��Q�����E�0�}dw�6i犬̦�/�S��m��V�l�V��s^R	��cO�]Vn�NW�-���0N{�+m�T&x���<�èh�|5pM t��_���3fu�Hf��.� �[r:���j�Erd�!��w(�D�߾�8��A�	3�x�qޤ��\d�9�
�����si	.�����_4��G�ηE�DK�>��K�4��zb�-fY#��M<�<鲕w((�G7@hv����([AVۇ��Měkz��f�ج(���E�����M�cfo�66
�mIa�n��u�v��G�r:�D?2,AbC�h���������I|�&WN�,�\�������I���%�ㅿi)��u^և'�����Hy}�-7����u�\ך�S��3�c���D�AS~�η8���َ�lK�[)����W�B����B{����;�{��CF;�W���]ٽ/��>���^^q&!��G_oIؤK-�L[�,FH�1F�x��緭]����s�2���h�W��D���V�M�E��/V�P��������c��9*��1<�(BG��M��n�[XC��C��g*$h�A��V�0��������£�����fsL/���<�<Hh��*E���>�����>xz�=T���a�@���A�8�ϝGM$��?��&b�1��� ��D���M���R������L�}Sm�f��Ǒ5r�����>a jC��8=Vy�V�[r�����Ǜ��n[ �m�9���A�F�d�=Kqx���Fb\�K�:O�K��B�M֞�XIz*�|�����\���f����xۏ�P�<���zz�Z뜗��E���D�	@��0��S�>o��ku�x�Dy�<>�է��}�|�7ʉ6eǴy�x&���M�o������>�<�9<��U��f8T���$�ꎥ�]1eX�M��������"�3���"�︝�㵦6q̻&H�o>�Z ����7t�d��g�7�d��	��NPc}���wŃ���	o$��\�*,�m���AEw�>����a�wu�l#	r����N�4n��;�!s��ˆ/A�JT�\�[� E�Q�@yw�F:~��R��^3o�*�����J't��N�=�ք��whq�V5-��@!݉7�����qę}���=U=�����B��%�O!����z�T���n�)�8B��8��G��l�K@��J�j�Kv���� ���t����S�Q��b�[�/ֹ�w����HT��Y��ڇ��d9Y}�����Dz֢���]�{�y�1I�N�A�jmy����YJ����>m!�=h��b�Q��q���{ ��o5�A����x��"t��d�vTW�XK�ԕ\_�s�/�6	W.��[������g��>,�|�甪�r�:w��ꔽFY"�kn|�>�y�ʔ���?\J�݋P�=��A�dL���0�&W�/��*^]R_˕�s(mx �- � /r��1-���!��G���T�tS�u�ݓċ��� "xݭ��DA'�FV��\��S�~��t{��d:Y����	���&K�,J��?0+�vnf��m&���a<��{T_x8���
`@@���6�FybG�O \ܑM��A�L���.��7O'�GLd׫%�XUz<&�[.-����{�#����L��._<wAA�ܔ5E��;8c� �w��6�b���I�X�qT���{�� õ�Z<#�(��(\�R�.�pss���-�B�l%�\���i�h�Z�W;��O�׫��.ad�|��Rq���i�������{ �J��^:3���&.E�J��å�h�2�Gl��tќ]_2�޿vA���8l�R�&�M���v���J��6p���P�5���l��NF�i���M{���6mْ���������P�i�5s�gc�T't��ʟ��=����X�0���
`��;����7�"�b|�ᯐ����;;h��8眻h6�%�VV�#!��$w�m�� �
{�	Cm�x<�:�e2{�髳�#]���\u�Rm͗�A
�p��a�Xu��k p�̘���;CШ+D�O����$S��8ל�$��LID�o�3**4C�tr!��%�'�w��愙�BO��-V�M�p;lsX�,���SG����4����i\N��)Ԋ4�R$�����h2-���pgU�^���%��K�W����Yb��o(Ԇ�E���N�Ҧ�����Vu�z?3�
)�'-t����t~WJ8���[�Jdo����^j��_+<*9���ϓ���8�؄P `v�\�z:"�#���B{�S�.�p��,���݌��U����x��+GlBp���r������<�*�6�)��v/������aGA�8�5r���S(�q
���>!x#U�� '}<@N��G~yZ�~ح�f!��%D��\^���q�y��#�a=�|�,cP����1J]�M��v푴�R|~�@���dQ�����`��I�!`�������u�{[���]OƷc�08�.����Ǘ1=3�m좸���0e~A T��Zo���h�&��U�ϲ#\*T�L��t���J�eR�c�°1�����h�?xܺ�\�].����|�ڣ�ܷ0n��Fz�[�ftO�m�z�˗QF&�`���۽���ط��f��ۇ��{�c�� [��8����RS���i(G"�e����P.�[��B9�G��V�g�h��1U)�c^��ִ�)#S!��팹��C�/����F��#2�A2F	^�G��54����}|���'mU��9�&�C{�?M�jXf�G���<^ʶX��ｸ�-=��/?��`���5;h���c\.Vv O�����N$/Zm?���?W��1��<P"^���LA��h�:�{�ԗG|G74�i9�pi����4�|��|`)Yb� M��߫�岍�K�m��k�M=��[c������G�u8@+H����[�r0�@��R��Í��Gy�B�q| WD�:�8E�������ܔ��G3�9�D~�;��b[R!�؀�I0�����#j.}z�����!�����������q�*֊��*���|!��8f�/�G��C*�r�ap����W�t`
-����$��(�"aƢ��>��X�ɴkU��2��	wc�߶�[$�a.�گ8�6n9:׉�U@8>����M�N���R���Z跚.��DH ������@+�u��w�Su_ܣ�]�R:����vG����'m�Jޜ�T�E����W��`dͬ�����['��5��{v�T=l3p�´apw��{�6yL������BQ����Eyz^N���o���O���|̟������aY�_��dFЍL��ٜ }Ra]��P���[������Ҝ�}K;�Z�g\v�F�+��E9�+�Dh�𥉉x��<yb���@+)�8�*U▖�*�e���eo��.F@?׭���V�J��G�|}l��|�{���܆�����[�W�̴��S����C��{�������/2���T���.��J���
iM�С����8�Mf�a�������<84��qz�9�u��WU�}�����q�WRS���ͳ��Kߞ��_ˎ�tdRq���x�}*��K���,�t��y5�pnh���׆��>��@�J�pʃ�H�H0�p�	��g^���U_��Om���_z�h~�V��#*�3�K���TK��GKr�xA7� ,l4�xG�Ðs��a���(�;�`�]�t�X�q/�� u�S�X��z@d��")w=�.?r�����	���@3}��s�3c�b����%��u{u����d8:hZ�1!�0��F�1����&��qo��R�7y����/+#s%�ջ���_Q��$� ]0P�Gb�f�}�V&'���F��nd˻���m�3W�A)L�H�fT�"��p�K"���
zA^��<+�Kї)t�P�2�,4�}U	�	�/G7m��+J����[�9^t7�x��x�k�0ֻO��o-4j�3��zTL�7޻S��m�I��>rI����$w��k��l�X67�Uӗ7~��r>}��\�.J\=�&��J"�`p�NjHЅ�����x�Z��#�D��eKbx��5K�f��2�ʙ�e�%�̥*?Ŀ�����/p�P��H��&#�I�ӉR�l���EO�A<[9�i�9gVy?hm��HI�H<�n��~;�ጒc�j�R�m~de�}�z[�_��svxn�n�(X7?��]���An�9.� �{�Gc��AR%+�01����ҝj���`���u�ǐ�J����� ����2�y�cq��jf��9��>���,�c�<�W�B= ������;U�ُ�ˣ�I���fT{�� ڎ��hT��
qZ7��w�(����@�x�6��-�u�C���Dk|wn"�%��]V�"P�>>񗿅]""�p�;m��p�|�g×����/�$�p��G�4M8���8�7C�X�Tnr]?���pH
s����υ� ��vym��=�����~�L�5�j�=��C�~{�5�r�R�}������J�ށ�����'��&4��3�B�x�l�k�g�gGX��N�U�O�*v�b��e1c�bh ���b;�z���&��KwC�������VzqʶM@�X���H���������'D�ݎ��Q����/�n+ZmVz���]����Vo�+�PS��_����q'�y�m�Cь�EK@������߾O�}���q��d-���߹���n@S���l��1�ExM
��|zAQjc�ެX=QD�eq4W�	��p�.�1��zh�avk�X��vy2��-g��|��E�u�w�������J�}����m�M������EKeX��8#h�Iʼ����r]Ѐ��u�np�b��Up=�8�f��Ա9�c�����im�TĦ���N��26e(�F�^̐�Id��؝p�l���vC	����߅���7���v;��ڬ^���x�.E��E_���*��>ʛj�=<Kǖ�D�-�}�m�#�=��'��k�;�F-����>Z��Q`��'���
c�i�p�����\����,{���<7`�ս��0}��cgE�N4�k��g��ߣB׋)W �kf"�~�H�ӭͻ���0�I��`��ا����v�_|�?ǈ\���=Yԙ��\���,��5A�$�BJ�i�����<���<�@�9����1��/���5�77J���iO�&�%�5B*3����Ѥ��`�2� P���t�"\�&�%�΄C&=�>AѾ=��g]�/_�b��$[��8-\?�����F���)ץ�E��Y'h��<�;�ތ�*��*2l�R���*yě����J�F���j��W����,G(��ǟ_��⯟o�An�[�u����Θ�XV�{_��a^��V >�d����~�_9;��o�������b��8ݴ9��7���1�&t��lTZeb����%�5��"j$�}d����ӵ�C���#� ��%<�+T�������3���Y5⦝��_y���O�i�Т`:�*�C������r.t��� ì��MP ��Q+�5�6�\� <�[�t�=)LUZ,{Eާ�Ӯ���q��1�C7t˨�Y�5<������aWx�ɾ�ұ�a��5U�GG��x�9�=.�(p��]�`�4��з�:�"7�
p7*���L��m����P��c�dcS�`Ӧ68�=\΄���ͮW�ǜ?�~Iw�<w�A�3�t�O Zq,���2%��`���+���I	&Yzwo��ד[�g�z*1̶��)}�RmV���v��D�����gm�U�PS]��w���s4O�ύ�O.�3�Y�N�UM�#R��aa�z��8 ��zդc�qXŕ�#�|��j�?w%$4}�� s��H|�j|��}'o�����Ö�Tb>+;ͬ)�`x��KV�uʓjM`��)�#X� ��/o|�Y�4�\����>m����۞}s9"�y��(^A��FZ ,�C�f��<�4E$��hc�?�3�<S�z���N=������iM漋�O�3�@.��I��aGYyB��������X~�u$�b�64�R̶�O<'t[�m�b,=�o���{TeǷ����"�v
^��۝��!���vW��T���d1����ZK/8�����nB �K����juZh�(('����
'i����P^�ɴ��Z�y�g�W!����,��=n���Sc��U�~ƣ��'n;Q�q�6+	è�~���ݡ�Z��	�Z�E{S!\�@c���bz�G�@R�����N���91-.�.�YHMk�i�8����#����S�O�&(�������!Mo=o-
�̜3��s�Oi�
��Ւa~�)�z�P��>��sꉏ����F���įZ_���qȂ�+���۽����2�4j}!��baU�'H���1)ۛ\~�,Q/8���Cs���캦o�=�0��u�m�,§�pPr�z�*|ȁ3Q��`@ ��V��!h4��Ά�_�_��a  �*�L����@�����(J8�A���%F̾�!�;ڻ���l�и�6r؜� #��{�QwEUi!~���Ʉ櫄gv�� �E���;���?�<r�D{c�p�=��چ<N�'8�z/8�uK��ۛ��Śm4X��ț�>�5�Z��<(xi��EFYK�E�����M����_����S�d4y�I����2(ξY��]�;����A����!@�$$H H�|p������ �γ�Z��gծ�j��t����KWuU�����U�Fg��6�^�`��$���c�׋qt���f�v��7����Y*�r�ms)P���yk�7��E[�)Gw��4���ڞ��W�z��}�������Vm�����S�3yQ@Cd'�6���als�{W�u��n���lr�M�G���Wyu�b���VU�,���~�L�@����w1�U�u������JzW�@���C�fX�{�J��Ft�gm�-z@�5�NM�pϞQ���![d�f�v��p">Y9�5u���I��Bl5g�b���r?��1��\:_.�bD6Ro�F�sg�1ŵ��j7����lo��'�ӉQ)���>tH���o?������J���-���a�<zs�K�~-.����`�����*��*.b�}�0���tmZ9��27I'i
�Z��6��.��-��v���ӧ_sO�U	��/�ŘFf�\&<����q�g�..�>�K{�}��"��1�D�i�4��Sd�	�ؾ��Lx��y��y�5�RD;F4���̌���Ï"~���ֵ̧=��]U�ߞ�6��>Қ�0Η���	���q{r�pY�1+x��R��;���}��������9�j]��8��M���ެe��M�*�h�Bh-�j���Swa����Ȟ����d dg���i'6�E��Nhsؓ����HP����S�v�y�e������	�o@��\H���m�qh�%�"���ٟm� ���raO��3�9"8��7r�?�G�a���|�[��}Q��'m�4�#���-^���\�F�ޛ����Ozg⡛����kI�@iƧ�o�q��g��
��E�y��iJ�O�����1+
ܙ[Է���S���y�.f�e�����3腌�|d5�6��CQ�QH�Mʽ��d������9z)�ppߡ�c��"�/�ϕK�g;�˛���)������:J�(�8<�,S�p�պ��g�K��I��oz��	f@"F�sKq7�ai�2.of���Ă��::�l-��ޔ�tFnHP�L�.���k$�}~���λ�׊��m��j(.�C����c����� h��!6��{UM�م��r	����6IA�;N>��OI�l�g���Q����"��5��W˞��v��vo,���܀�l] M��-y+�2>���9m�����'�ŀJ���G�gl��������
�e�=I@�}a+��1U�NۍBK�����_���`��A[F�"ο#���*'��J����6M)w����7w��烅TYS�3o]�,�/�T�Aۂ?���D��ܠ�u��>��١*�u�W �Fc�@|�q9���^�ܰģ۷�3	A�e��8� b���)���>��^#���.���vT^�<�`�Ș�c�[���ZFĔf���~g���̿��h�����r>ߣy��j��ӈ񭧸��/�3=,���-�'oQf\A�a�$��IW[�?�L��_MZ�c���c?�n:I�o@W��ZٟWj>�drk�W��=��F��̢ ��s���P��Al�-�zY	2}J;��#S��;�;�zZ���T�㭹�9ҳeL�}2�%�|/�wR5T�y�4�w�nA�/w\3�z�Ҙp#�"xx
>�x����Vb�H��o��
x��J�Z>V�]K���~֖N�q PR����'���Ѿ�VYɔ^�?Խ5le(�� �(
��u>)c���Ȏ�#�s�w�e0����*]g�))Y�a��~|x�M��4��T�E!����н��B̚�������O����7#Dv�8�;����z�0��2\̦圢��ƍs<' �J�q�����n��0���}� D���n�jmu����.Y����Q�q� |h��ȓ�#�v�m79/t�BV�F�(eKq���eZ��Uo��'�6 R2솒�3����Q�~<0MI{P:�gr��;�J�ڞBp� ����׹w�$�ރ��!j�1���rqtrᩓƋ>K꯻�&�����w;i�g�_| ��P=��w�� �]��sl���7�֙{G�x�ҠB'3�*��W����L��G���>�8���y����Cȴl�6=�K�[� FL�z#���eZ(�?�s�E,�hr��"R�I:{SWU7��j�q
cGvů�[6��V|����	�eO��כ���:��Wo̚�$2}���Ԃ��=d���Z1�ϑ"�uvJݺ������_~����T���z�����M�df���P�5d@�g+��gy<���΂�$S���;�%�tu"�#�
�[�����B:�Ɣ��<�͹aD��A�~/UҨ-:�����f�_c«rl��6��^@���C�T��ר�X9]�I�^�d�!{��f�ж��K�6����M����Y��j`\n�}�~����r�|�kε!��Ԙ�89G3���{��GUX;A��c��y�j_�����o{D��x�-_�[d��MR��\���D!�F�W�F�v��dʩ}|6��%�Ԟz�%l�;o�D���mk��,��dΩxT�|����C�Z���Dq4�L�,VK>��Fⵌ��'�K4����i�Jz�����<�c��,�|R�˱�~ 3o��� q�7�r����3X�p5K���sG���é�x�M�.V���� �w�����_7�����:�h����;�4���ٲ�9�5=���w��T��*�ߵ��4^��^v�Y�}�9A#}���=��X����VP�۞�:�8��0�0H>~�0���6j��������=��v&&XSmM	7z꼪�$p߷��9��!$��M�{n�u�m����+zf:�������v�;���A�&#�bBn��8�VAB��ZE�`���|W�u~�c�u��b^�D�!ї�yIlDnK�}��V�o��ɞ*M���+�A��x\�Sn��e��4{>,���|4�Y��>"�<[k-_C��4��QL�:$"#뗊P��-�^M��=n�M}�]�4�	�����ܒ�M�J_�=�[�bg0K�������O3��N=) h6J�|2D�O��)��N�w�l<$n�6݌ZR�T���a٣aY��QC�v赕��]���jc`]��ģ���n�X쳄�@٤���0F��pH�{�C�����n��4܏,��H�r����>�n+U��*���1X>�b�0��H<!Ǩ�f�o��Y���ýe>/��f���T�KA��3i�<��Q�������2�*<w�W�N|�&ã�lt"P�׃>v�H1�'����g��ӄ�t)�џ��:t��e�LH� �Zh��Bk�����b�y%�L�P�}v4F�(�;�|�0�D�'�Ɉ�1�"����x�8�NB�W�ϼ?��O��"��6c�I��aD9���e�V��&S�o�I��N��KgG����M9M���Zp��;6�!���py�8ϾACRJr��6Yv|
�l�f9�%�z���Pl���]"��7K6�\�N��i���x(�����Y^!6/fn�w_H��v�l)����v�HʸU�C�^#^cxBH��hұ'���X�2��cJp��a� d�$5V��?O��I�_�)-@��E�f5+�7$����D�3� ]��b��W��ѳ͢g�f�}�q
�U:�r1���6N;��y�*��lZu{Q�s;)���H25̇�P�<�sB���^;�h`��f����ʇ:�IBY?�_4�yq��ӽ���f:"���\��0wC�',�*�).�hY�$�@е�d��2�Eӽ}ι��\����x��PT����rv�n���٤(y��+���^���f�a�4!T� _9�
G3�XW��C���D�T��".��F-�z�����QR(X�}�1�������HR�}i���m�c�Kæ����h����wC.95�Ѝ[τ���+�+K:,�� 5T&<�A�?s�@i��%͍IC����d��|�9�L�����𩦝�~��jhr�J5nivƋ��={zN���nQ��a�\\/�T��jntR���b0MU7B��/�>�d�+"9�ɤ���2�'�g�r1�RT�@à=7C��UX`��Rj=������2�jQs������\:�[-%�FwF��TcD-��{�Pq�[��E6�H���=m)�K��`Ղ}VTm�X�&6�J'�C@�'��"1�:N}i�o��E
ޡ��v,M�'�_�]��/_&�.h�"�1E��!�Գ������S6�ZN�������0�؟���H�/B���e�zp��.>��l��}ǜ���L�֧��S$N/o$��6�QbCv����"�Z��Ct�X�#�(���~���|��t�22\�~" '�E�1���X�t�{q���{L��eY���3��$���eb�!=�V��=Q���~MM������H�,�wgF�1�pv��� B�"�����x�	��>X3�WR�z��`T~���v��Q ��T�lt�Y��++\�90+b��P��r�^m���EXGw�yG%R��E6�P��H#H;5VS)NtI��sU�M�V�J�b�Y���>ѱ7�(�FNL�@F�Y���.����n��]#.R�W�)A[x��Y�I�L����,��z��a��U������l�>�|�"�;������� ��u�9�&\G�A�.<=� ko��AaV��o�{���C4����0W�fKT��'����o�_܏J�]��\0�ʡ���OZ�T�N6a��(�N�c�V��V�|�X)�H���R��綔��|�F���;Z�O��B�h�7��2G���ֶo�:����稽U�&��_�a�}BD�����K��
�f�L5�Y���ȗ#�[/�[2eN�h�t�˝MEW�׿Ȕ{����J�|P��PV<ᡤy�G�M��CS�Ui�oؔ ��e�ϑ����ĊK2]D	�>(Ͷ$��䓽f8�(����xi|D.�pg���"��ԫlsT!��rVˑ�j/��J��9��J��9�$N�Y���U�?A<�ku�4])h[k�-4-�+n���:'����W�eoT��R�?����g��g���፤�o᱌l�Q�ah}5��3�sn����o�,�И�1gRh�(��`�
IK桩�h�&>ΐ�*�$?�4Nk<~MyV�d\��L�tsS�1�h#W
��1�b����:��/9,����-���@�Z~���;Ӳ9d��ǳ\��ݧ491����	��t9�,2�I	��:;ݭ|�<G�'2��M�����������g�o�������q��h�ةS!�-2���Jԥ_3ߊe�븦M�@'����g�j��d",�R� �י�J�)$�.�/��pb�LpEB�,���K-bd�+�+=(���n����
��$���B�~�MDˣ���s�Ǩ�#J�|�(w��	���T�!�'Wv՞��pF�J/�0��H�h�,{C{Wa!�@��~uv�O'Ɲ2HY����|8�& ������Z94�Y������~<�5(U��c��,��e)x���ig��޺H��{]t|���9R>dt�s�$vd���i�Al8�f��_	�L����o�	�J|�����5rg���F���X��P��íܽS
�ӫ�%����w�@(���DE����j��"ss\�!Ɯ��;Ք��t^�cZԦ�:�Y�2<��!V�tEۜMT����o��°�i�bu��?E�v!,�Om���ļW;�=@���4U������y���"|y��U,o\���+�\��*ծ�PF��nm.������ȸS!��R�t����ѡD	�R�#�/	�Q�IY�vA��\�Vd�ъw|��=۶�s�ܥ�?UP���qGw����Da����k�"{�����2��^n�;j�a-D7��������W���t�9?�l'[�鿣6�NVO��K��~������E�g�]�Кlk;�7��<�?V�S�����3�r�m��S�#�^�Y]�a�hک'V��R��������U�~�})����X/��')������L�E��N:��a���&I5�B�.�.xXäxA�?ޝ�+�(>)}��^�6���:�.JS��5�Uw*�%5��U�!��H�� )�In���M�7�wJ;Yp�����-o�HȢF���SA�=d�U�ʾQ��D�u�h-�/`��#�3���)�ݬJ�>��)qdhK�=b��L���g,���Z�zzQ��~,��1�\v��[�N�ٱ'C�il��}p��a���%�yW:�����C���5��%�k:��� ��|� b8o�_<�w��o�<��H��#KI�3�х/v�|y���[�"Ϝ8�Z.���R�q/�ѫ�����l�a�{H�ml��ف���<��T��$x��X_�OM���t��B�1qaăҬw�ְ/���x¤�Η�K�a^$w�Nz�sS��e4b���99��"g0o�� ��Q/f�Ӳ��=�S٢��"]H^^Ǥ@B�P���e>
�5��_2.�*�|�bb&#���)��X��}MCʽ/�C�R���^S-t���q�.���!�X�3��=��������P���a�7z嫉�[l��Cf�X{��V�b]�L�V�����t����Į��tzp�F�R$S�Vf0���W�E╧�
�u�)%��q].YP~�3n���+�oP���|!R�c؈䩆�P�և�q����J����`lM2�a���5��hL�V]
���D'hv~m��jHH,Z���B���P����^��	i ��{��Ow���=TL�ԨP�*T���6�� ��0���W��9�@Y��U�.#Җ9�U��a��3��W����n$�m��d�e�n1^�����Q�ţ��u��H�T�Ja��QY��<��,\x�Z�������2|>��r"T:����>]ݭ���[�!�B^r�2p^
��5W��,xvf�$���ؒ!ǋ�)��ߜ��(�'���Z{�kl]��Qk���`ѻ�%o9��"�W?�d<k&����A���x<�ŗk�L�������Ew!Z��e�ȭ�]0�5�%  6������%��˦Eϝ���ӳ̴��)���񇴧ޖ�w�/���b�&�N�:C�ol��{��g�<��F�7�'Vd��9��VC���������Da9��T����k#gl�!7�^CO�L�4x�Zt�	��타y,��=�d� ���z$�u�'|�
���nC{sƄ���°Ԋ������-:�2j�;���wx��H���~��-�����\��V^r��dLo#�	#�sp��M�{�G�a�l��F�9.3eڻ�֥L&ڎ����r) �̢�CX�����1TO'N��T1f_�n�L�TI��~ o��H;C�|C��}�PBm4�U+��A F\ݾa` ���Q�I`��Ǜ�"_��H��7(M�\��G��,�"ӅU��'A,7��,�Z����?������xkKDz�;�;�Fa_�b�t���ڠt~v�`���Xl�i�|��\4�{oc����ޭ���)g��ϑ}�V�]Q󌼕A!���#��3�5��8���L�I�ŲMu�:�K� ��X���1B���W�v�+���*3�,!�����W:�P���,��
��"fCV�a���n�C}[�"�1�b������rj{�:8��/�]@j1?�� D�K�#��bQM��܆�����0�{jz�0���megr�B�\�y�x���T"O�@�d�!{B����,��Sm�bc�7��}���l�O{y?a��t��(,SĦ�n[�p�!�?-8Z������!�++q}Kί�.`��Lҽ���B,;�,�L�j9�ؐ1���º����'����������A�3k��S4�LG��u.w������g�.I,9� 2���mW�wQʥy�����&�������s�"�b1�5�_�����h�rs�4=ߦ���gC���^�������a�H��d��xXe��ϑ�A��1��gƠ�@�o~��D�qn�bh��D9	'�����޷�����HI�d�����0 M�d/�COzQ��0���H'�ج���α	�4���2��Q5w>�⌅ʭl�/�b� Ģ��>ů�ذ�7�ƅwEx�ZP�{�����L�a7����KY�6�-ď��iHZj��p�H��$K���z�����˵ ����y��Bn���	�����m�W�ߏ�4��>���Τ�.���v?�!����={Aބ �6�1e��H��;���U�ҩzK���Q��H��x�����瓏���ƶ�K���mF�&a������{Zˬ��!.$C#,�:�)�4��w�� ^�B�Ph	z݃"5�ms0]U�O���x�����-'HF���e����ɨ]iy��:��&��v:��B��Q)H	�.lcW2��K����7~kU<C�m�j�&[@j�0��G~jW�R-4SJբ���� I6�����m�^�f>��<��-fW�"55�͞��o~��1�+���<a>�&˗�������ʧ�����""�UN��E�	.���*-A\`R�}p����g�P�/دc+�.�$�k�#�#8$��ed!�3G P��|7�
m��7�x���1T_�3z�]@BhV�7�[��A����r�X��"��+"��s
btq����}���A�o�H�0�5��:�o+{�A|$��|��*�6/���ο��I��4��?�*d|~�����@ [P��n��k˂��m�ٗ�0�/>�J�:�/4s�]@�G����(7{oO�o5�;���8']�����ѓB$�Zp�;s�����Uɘ��.��J�4�Ur��W��{E?�u�y�(��qͼ���	K��V[HKz�o,۟�Ki���/|��<�rv{Y�W�*�zt�ZE}a"2�� �:|��p�v
X%��^�˸���ԯ����
y�����B���-E��� �%�\Eyr������*����lVn�-�����7�2$���\e��s��-�FξӉ.H�o�aゼ�?�t_K,h�x[�l;�-X�pc��cl:��|��2;�����md�2T�fOD.�;��Q�9%�"x�\�PzP;}ܥ"�L� �|�t�o@���a��^G��z2IMs�@�(x~+��zoO��k�eT��w��6�f�X�B������n��}��
<M��5K��m�d�$�#�e�f�1m�����pLm��K��fጇɨ��c]^�v�:^��:޹�v`��`�mol������oQ�c,�0��s\(:w��f���CUxs-Wo�B�,FF2�F"�a��.�Ak$8�g��M
;��!�A�erT}-7�F~�#C�P�7�x��q�E������79D����Avn��*gD��_�j���{���Up�u�7�C�)����!!��/4N�\ň_@��,�Ad�J{�3�Œ��d�?t��=�&ok������Et�j�3O� ��,�f��������ʌ0���x�����\d�&��^ѡZ���t�=����-�ۯ�":��h�^M�s5����&AS�S~��O����i|� �P�-�f�VΜ�M[�e��jhk�2��T�56]��-�eT����?Hۋ՘���6�V(Wz�M�"�r����	��})��7����)l��dnh98��������l�i�aG��L���U6nd�W�j���B/K�9a�T�N� ���ml�����6���&�u����AZ�S�RUȊ &���[�?�g�t��H*�J�k6���{��.h��o��ޟ-M�+����bߕV(A߸7�K��;���q��wQJ�N�>쯼�S�+��m�ZX�����O���}���TB-�Y��%�#�܊�N\J�Μ�TH�M�9�� ��E�j�7P�w��^�ޒ�_��b�
��$,DMo��ҟ������	����W��ǥ�V�&�B��~�0	}��C �}]���M�^��t,��������L^�ⰎP�9������J�v/J��/VԂ��W��H_</��Ѵ!U:�.aX�Yc�LRy��dg��V�VU;�t�Zo��V]N=%!b�#O�Q�Xm�X�?�A
COH��4�8�v�P	��s��V[�
t��9�{��yh!���r�U1H�����u��y�,��v��`-&���_�ה���G�o>��U��w��E���Zd�"�aG�Ģ;���p}�P%~/k��ٸv'���&&�)13�ڜI��na�c��;��Ѓf����������U�OEgF+F]�e��0��\A�q����$�Ӂ��I�7�����`���h�!@e���f���x@^�y�����Soԫi���x�혊fW?YF�Ic����f9��V�'�ڞ!#{x�&^�g�rǾ'���h#��좫4Z+�7��7��\ei�yģ��Sh���S�sx�_~Pr����{mKhh���^��h��Y����̧�lQ�Sm N!�M���.��̣�[�P�5����1��e����������{��:Z�y��N��c�8)���l��86x��Һ~y��g�G��K����;�YgI����]Y������P//���\�͒���oY�dѶ&.�����V�#�5�|eO!�������.{M:1.�M
�����a�6�L��#��8�+ΆH�ܷ�/s=�����$��k�P�8�7*��-���?�����V�O���vh�!�[jko����(�%�7�����${|2��^D���a�u�.wA��oi��Sa��c��EO�"�4�v2e�X��%��hl�0)�5��~8xn
���]��KB���Q��q��_U@���3�]�������jܒ~
�z7�-�	J�/+KL�9���5�vW���Պ�\���3�i��sR��AZ��a:d���tg�k�ʪ���(Q�$�oL��]V(�٦D���:l�d�ORm�l�s��U��>  _�.1<^�Ov��5�#�ҿ�30�"͈�z֌��¬�~�^����p�x:�T"R�V(���j��q�5���n��ڋa��Zv(p�{U���m�*0^����}(<􏁠�m�'@a���Y�U��;�������s{�Fe��?�([~�n�@���X���V�O@=g�UM&�E/��*��\i�r��(�p�R����}��L���˫���l{�$�zB��љ��K�Y2B0M�W�f7Yh��r���9bw���?�m�:��~���!�]5���U�]VڥA^�3�pć='#��z�	�g�qŀ�N�D�M-���ikfz�ox��� O���5��=�!#�S�q� �v���� ��*I]��vb�*d��K�c��\��O.��� �k֫>�( �\H��v8Pիb}㉓�v��3x�>&���ǡH��ݱF����wh�*+¬w]���,�p2#g'�GG�Ʉ٠�5(���]���ʍ�4�;��[�'���)౏*s��==�=V3��1���7��O��lI��J�7��ĐF��;DK~,K�/��0C*bጅ��*��	����R����(p{#=�Х���OJ��v$�1Xx<6�o����o��Sds��[},�5p� |OG�����*e�3�ۏT<�%'��?t��R���穞^��@.���F�9ߞp(�$)[��\�ٯ�]M�Z�}���u�X�X��c�1�i�Ftb��Z�x��C��1h��[-�VLϗ,��6�� zSM���5�I=p�E�h�w�WG�i�=���w����a�=�A�n�+�N����C���O������>Rr�_�"�² �����Y1��tjd���a�]��n��4FgSn|�i�t�a�ZVZ�c��BH���[R6�>Ա�6�|�'ip�Pɲ�V<�@��+��>Ξ�
d��	/����~��hk�/����P@��0��}WS���su��\i��W�1�!��	6w6�;5������/V=�?N3�4�6J<Z��xܧC&��e?=/���&�Oh�X��4>}������??<����}�!��j���Ss5˺��B�1S���d��%B��1��+��G�w��u���ҥ�dC�ޢ�Eя-<p��N�ʱR�>����j[o��w�%e��-+�&�6L}`V�3��!M+��c��'ʯ�].λ��L�����S�Il��yZ�&�Jd���K���#� N�*��`:��Ν���4MJ�M���_Pl��J	����k՝}�OJ~��Mx���;�<��%�-����O�������
�MдM�Z# *SQ0��P���z?J�]˗�=��99�+���,'����w�?#�j�"��Uk��Y�]�mi�;Z_CI>^�F=&�@	�]m+�_�7�Y���,^.r �*�jP��f�z�v渥�ow�Csg)8���Ggq&\���^�FY��4F�[y���X5ح�����A�T���S��{�����3'�%�M���Lo�jK�HH�zߌ�₄�!�n�c�
��^.�>�9};�k\���n�AV�/��qb,��aT�
���,no��&�-�P���x+ivX&�/,����{͗L��~�\w;���=��s1���ҳ�6�11�IP:��^�)�9[zдx�$�»��L��'i�"�&�>�<�f�X������E�_�L�V�j\B�����Mʩ��f�)B~�3=�=�q��۽�8%թ��HB)�"i0w�lf��fЯx:��|��q�֜nF�@�K����ޤ��r/~�|1�f_�R .P Kd�`_�uW���"�a�(�Cg]@��}����็ڎ幊0	o�\3f㥬B�YƳ ��<mѐ�<hm�2aR!�c�sl����\������(V��	A�>}��f#��<�;��1�>���9{p��R3�m����mCr|����[�Z��+d�i�K�n|�$�z�k�t�,ă�N�"Zڏ�z��纉����A@��ꍁ��`��ʺy������WY��K�X�Y)�I�S��ɤQ�J�[�I�ˡ��Kt*}�}�o�+��_��ق��L�MB/����S�H
��b��ŀP��Bu�=�J�1K�r�S�����	��r�3?U�Tm�P����G��~��f���A�e�\�����@]���$�PWļO�U7�O�
���Ӏ6dF�qꏠA�f�5�ڶ]y&(˖�7/,5�9ӮP�d��V����ɂ�,˲!�!:�鍗E�]O�v�ZI�1`44"���&�S�K9գ��1B�\�ť�ɚ�6��Ra���a���(/�;E'���@�#����Vx�#/�xd�'=��#�۝�3��Q"���?}҄��\�sW�
2�W�L���A�R����յ�α˻I���X��f�nX�Gv�γ�>`�Q�5a��U�@H�����W�͕c��N�SN�e#�&�����;��)�F�e(u��
��ݲ�#��t7���J��"<�D��8��6�L��}G�yAuTX���QG�U���%	e��D�Tb"#?�ƧH2�MJ3d�x�̪o��X`�f�x������(b�Ȏ��&<�a�a��1�}� Q���oq��/CAd��amM�x��;?���k}�̫�c>� �J �׎�͐MS�4�e�8��h����ߕ���/it�M�3xc碯���X�"ܣcE/�/k,6�:�N�p���My'VYx���7m�wZGsf�3�R�Q�����l����̖�������-�t��h��n��o��-k���]ȓO:��8K���7���`u(��O��t�T���Z:%������42���N\���-<���k�|�E��?*hq�L{��1on׊�U.T15Hxw������������B�,� �*��uA����DSW�1���*��J:���u�O'@�_��㐔#�����n^�
Nc���������?��6��X��ʘ�j�*���vH`��0Th�mW{�29���s̫&�&�u�;����=W�X�J���2NXO�R��:�4�6I���� �������i#Qo��
�zc���k"v4@�7x"���0KI�����Fe�cqN�yB�8��7P��~pduC�
���}j��>?��N(̌��5�� �dF���!F�H�q�P�8���bRe5����U	iX#�����M��-n�\��'| Vw/Ё~m�Q�@m�u��\�y�+ذ(aÃ%K��5q����8��&b1��;C7��9ڳϋ��)��XZ��1C�j3��!���^S���f�Z/����|nӊ����h��1���G�u�5֣R�$F�z�$�����u8C��+ҋǔ�	,�7󖗳�/��ml�Ԏ�g�d���BwuO0k(�x��HRjG��Z�Y|]�ɤG�nG�Y�n͏ݰd�u�H
�
(x�x���� ��Ȇ�E`٨�Q�d2?2U�l�O��M��|�H�Q6C��)�����d�
ﻀ\\��tv�`0��q���5j�]�RRQ�.��A󏟐�,��B�U�b�^X���߭�Y��$����vp<_�Y|\8z��?6�/�/��,G��~N����V����M�
r�$6Zm�T4~��[�ՠJ�c��+�5��=���L^um�0�FE������8�w*r�{rnn��o����s��^�Rp�ťq����ڿ,����3^��������v%r\m�:1�`���7/s����f�	<�l&�X g�L���Y�ͬD�/Z�;����r49"R�t�&�H��oeUO����q�r��,vA����g~՟��Z�D
ݼ���OJ��nU��%��ؗ0`ݩP��f�n�IVu��*:/>�9�)o�*�l�]�w
�|]��ad�Ls���7Z[9��S�y�Vm6$� ̈�4ْ�=|��JJZ�/F��ū
�bj7�G񑅕~&�&9^C��cw��MH��UO/D���^�\�m17�!��C��<k�7�Rؗ���X	��=���.��չQ`�(����N�d1(����T �t��J�>���᫧�̧C�<��w�V��K�KMV�N�͐��I�� ����Y��0���ʙ(l$˘��y	��;�>��Wd2oh1���rw���^�C�
�fƛ]`�bS���E��PI�`킡I/0~I�}=���*��h�Np��u����Q�G��d��<�dD:R.�q��0��W��!�iO�VS�S���r�
���rp�x�1��X&W�]�p�V�8{r�~c�t�ἠ�(�SrH�[����E�H�b�CK�A8�QÌD9_�"����-�HFf���g柟$Տ�N"W ޚ����7�>?v~�3�D��T&\ħ^��"�q�*А[��t?��cQS��JRk��$~�i����a�ym@ &�"ol�_@YK���$�Ҩ	�9��I'�?3pn��7V\�W@��&�.�	����*<P�E�͑7#�_B�e�q�;.����"�(T[���s�׍�2hS���o#����U�!��S"&qk�?��TtC��R��̺fl&�mL:�g�V�������_XLZ���X�e�r3p�H����
�����u,���L��<~���=���e\J�I�G������.�:`��gZ�º�=-���,mD `h�naG�a�����;j*V�fx�&'�i�:5i�9��لaA���*�����`I�Q��?o~�wl�z�P�ze7#�0^\ԌS ���O����QI��-�oR�.�]�0�X���C��ˎ�(�ʋk��dk�1!��[��+%��Ʃ#���}�A�t���j��"��� �Ѭ����x��;��rOMrY� �f���ĩ��M�(4�,��L��2�Z�O����*F�3���U+�9��\���]�ej�<gjM���f��׿���%BgY@�kO����4rpQZ}s~*%kh�zjO��7����|����b�/�Y�%�fo���K�ů%���_���#,�^E�.b�����N(��kv�xM�1Zd�(�D9� ~G������n������[V_����/�=��Gv����E�[��)��C�n�et�Q��~�7|�	���>�c%� ����B?��\�#���{S<C���w�d�2�Į�'��k��h��l�SW���`��z��\ f�ą���j��Fyvn�&k��E�#�4�¬]ŗpz)K9�s��%eЄ'�2 �C��s��Dd�b*��! ���ݓfP/��L���#������#La��q��޿?�1a�����`<WP��Ѝj�~_�?K}8Zm�1"h-�o��p82��`�t,���������Gk�W�(5a�.���-�	�/1"���3Q�K� Ha��5J�$��轌Q�F�o7vϖsv����y���s�s���ߏ6:֦�Q���W ߨr��3X���Bf>]( �,��\.�>�
�%u��O������s��Ġ� ?x��v��!��׳��5��eЁ�2AXYVc/�(F����kg�U��{��\��D�>�Unco�����=ῤ ��u�����q�I{�qj�FJ��u��
�C�=�z���d�
���d�Q����(�WI�Y"��X�R���p�.�ZH���s���N6c��D>#��k&RV�R-A���R���w��j�Q��(0��(� �qs�6��񅇖���+'_�db���`j�������Q�;����F�P�����r$֭�+����L��jޔF���\�V6n�z�#O\�+��W�_��� |7���@D��E��ݢ�:�9��ɣ2a�L9����߈�c�/��N�Fz�V>M�κ>ǪcxL���x%A��k�X���[��Sx�O�ݣ\��r��dwǭc�{N�}(�l����
 �^�{�hĪ�P��Ǥ@�/��;92s�OvHo����7U�K�כV���Ŷ�+��gS�c��%�ld@D����b�bd�O�/VWq�($�Xg7��v*T��.��H��}�}kd)�P�#^�hJ%Oh[�Y/�zph7�b,?cY�ˍ�Y6f������1Bb���>����(�ƹ��}��Ԉ�Ay#�_��8Qƺ2���z_��o��u�|N&	(�����j͘�'3+��Y�v����L�8��	�,�nb������מ���e�A7$�U�n����z�����Gx�(B÷����#�Itڽ���ahH�	䋣yӲ�[�Â�r�"�-@�e"����mcJ��j�P�V����7c�M��S9MTj�r�K�4����tG�w ��y��\�Q=�=���&�j��� ]���}�S&�0w��RdV�#WC��.�]��Y����yO�{޽�Ӷ��i	���X���QZsU>ju�&�5Ҏ��-��B�����p���~�͏_��}��3�2d�=u����p�̥*�"-4�����>Z����O�P�K���H�L�������f� �܆��("�yM$�`��|[Is���n�P�%+�#Պ�� U�j��H\�,>J�Gc,	%[F�v8Vw��#�c%0,,����7/y*����fD��#b�)�����t��FD售Y��{Yow��?஢9zz|+�~i�S�!�ƹ�6�*S_ }K�>���b�.�"���ZZ�Xr==��9*��{�x(5��U�Ɵ�����C�Ĩ��Ŷ�o*�u��q��W��rѬ]�f����֏�!l>���Dw�Y�8��%�i;�v�L���K��k��Cn�h��"�!��I����U��7]��ʘ�N���&//V�S��,��2��L�i�v�\4^?�|a�^Ń�(�P;پp�	]�Cg���~�7 {p������t�"�l�ǅ8�A?���)ܨ��!E"�Ha���U�4��ْh�s:k����\2��Sܻ����`�D����$�GE���$�1oV����{�u���8%�4� �P\����Z�v�hǖ��ǈ�S�!��?s�ԛ��\p����/e
�Z"�?�q�^�D9�CX4�E3^�[s~�X/	��pG�v��^wzq#���S��ІTv������v|��x��eT�0X���uӐ0O��^lg��^}6\K�Ǽ����>���?O�W�\,7����@OS
�Ǩs��Ta�0u���RN���b�wl�=�F��]�2������-Q�{S$DX��(�Z�V|��rd��$�j�_�խꥉ�L�Z�Gkň��W3�T�c��_UY��O2�F�M>U�ܔ�;����P�g��r��!�T-�u�˰$�&�D�\�&����r�4���_O�5�x�~�Vm1��Ѵ� ��|~^A�l�&��X��~���A;�b��G?�AP ��1R���ؕ�f��TO��(�H ��=w�NB�',\��Y��E�#��KG���0	�|
��A/o�B��c��]�P��%Dg�ߤ��FeO�I"�y�}�O�(�Y�M.��q|�2��ŋ��?d��n/�j�޵�_d�����+ߣ���Z����y�"�^��[9Z�&���)n����ĲI=����[�ڴ.M%
���[Q�@�����n�jౖ^�N���,����?+'��	��B����8���a߃�P��<=W�����9Nv�kxi8�r!���-}7_'9ol-s0?Y����N�}�}����M���p�0���-G����1��㈀�;�5�'����ȑz�F�7s%��~��5�Ǽ��Qe�W(*�W�������h#��1������N�9˱��z����+}ۥk~Q�Ɯ�������Y4[�̙ i\y�!1��Ũ6B!���g���6��n�q	���1@���Q��U=
��˖�ܦ(<}/ݮ|�9�3�t������s1��#a�+���
Eo��;�݇s���9��^���q�5K��>)���|>g��$��wpQ�}q�ы�߬�M|��d�X��(F����1�kH�o���i����4�a]�4_���֬+�עH�z��<%�[����插����C6>}�_ń�S���"����-texX]��<?�x�K��n�qa"=��`�� ����i��z����S��V�d�|�������Z!5}i�;6��O+qs�^�O(w|�j�b��'������Y�t��2���^w�w+�R�<���x[hL�|��U�=S_��9�ڔ�DM����~��Y���0v	zfFBx����	A4����Z9J��ʐ<�pv8��~Y�[�ҕ��z�g+-d�,�Tc%���?F����?��4�G���o;���N�
�Y����TE#;������hHOS@_���?��-.L�8{����Y�@��2����Q5-��!�<g�Y�eو���6=�W[�u��p>�Z�zT���]��-�N]H�WT�,'=�RG\�ۛ��C�d���pe��PA�s�>MJ�/�+D�Zp���!ls���1,}kq��C������v�|B�]�8�#fM8��t��Q-+JUf�H%>RN��N�G�=H��aE�U6�a-����o�4޼e|�ڑ�9$
�0���exl,�?��ʉj�J�?7嵗�Y���⹈#����#nP� K��8E=��g����NO[�K6�cA���9/sjd.��8?d���{������_G�����}I�b_Z~C��}w��r�J�v�]I
Ǟ�P�Pt�KM1�����q_��:��0�b;�_rC�6Jا�o6�u���(op���|���q�`ݶ�"�Fޚ(��%O3If����4�z�<1?��A��5g�n������!ٔ�\+ (��_�͞c��.��	}��A�٭e������xZ��Ѳ�L���2W�;	�n����Λ������
%}���O;�j�t��q'( ���F�����$l
���o�R���u�d����Jr��N�i=|����*�z%-����L�����;��w�G��t��y��T ѯ��NWv"n�PZ�&�6�&@�}�z����+�����k�R?VE�
~M�kE�x��:�Z�p�}��Ö�=`7ڲVba�0�5���}U�2=�-��Y����4���;���I���d��W}�*����\���)S��e�[t�]�t�;։[f�ˎg^q��fIϗ�f^��g�$ew�	򔥉1�QЙA��ԓ�l�5�:�_R�x�����B_�o/I3���D�;J��&���${&��ߖ��Y}
�)p��Ѽ�Q��$�_ PK4r �(�  g�  PK  o��U               word/media/image3.png̻Sw%\��t읎:f�N�v:�mc��tl۶m���m��ܗ{�?�c�S�9���jΪ��(/������[JL���?�.���'跘����,8C̡����-��RRR�߽��x�������;ޫH�~�k*��s�ߓ�'B�=�ǊH�xt��tuP�|g���~��~��y	��l`���NS�IA1�O-R��M���2c�k�3K���yb�>�Y�{i�6���=s����O�Ȩ�$ Z��35x���'��P�cTIr��7&�6����V
�F�����g��7FK����9vr
>�0����!z+(!�����{Pl@"�#�2��AV����d�5p�p�����%$��]��b����4)��X�i7;l|��B�����[�6��M]�W�#�K����D�*��+j��N���"�E��i�(�yV��W�]o��Sy�=�슎?�f�K6�	�������-��NƋ����7�q�&� Qc��U�!o+K{Q}p ����Xel��������k r?<���&ɣ%,w-,>�Z�Mnwb+�����+ք��Cއ#+'�6�񡂮w65�~�@4��x!��,}.ҩ7��<��.�{���R� "��v	�����;�N���?'.��%�i�����R�p���Fds@i���J䈩��{u)�sJ���@���`�]
3j�;��;r��g �(�o�G���;�m�۲�f'A���:��O"���7|A��.Z�֙�}l+�>gI�j�>�߂Wq��B�9�L�CK!S�7�>�@�NEf�Dؓ�|<S$n�0e�v�i�x;�ߞe,z���>ݛ?��'n}���*}�:�E.�p�M�p�A�FvA~�˜[9Z57n]�p^ �I"�
�.�Vp9R���8C��jx���A)O��Z{��L�Vw�0l7���FώUҷ�	�Mņm���KS�8�OW�U=6�I9K����
�է3�Ue�ǔ�7'.x���b�ڳ�N-�l2����]@>p	i�	D��ΜK��g�SG��w+��<\\^�}ס];T?<�A�.V�Ì(J�`[��j+�"hI�OTQ(Q#��B�Ņ
� �+G[��o)Q(��v���^?�@��E_ko:=�ۆw�xթ�sI�Ycs��r@DMA0��gf��&�K��(��C��[F,��J-��+�41���ʚ_�Dm�����D��WѪy~lBN���/�����z(�
i�W Ƙ����֗0���Ʉ���;pC�?JqLn��>�����_F;��?�
����ۏ!���2JP�H1��6�XyC�H���sv��X�#��o���j�,h�QB7JP�� G5�r��L�in^~D3���׷�\�j7B|�/�7�w|]�l�������N�LV���X�Do�6mjy���S�������ݏ��f$���Ӳ0�'���Mٗ�����p�;Y�5ϝ�H�[���c�/�ϐ}�E�2��.�8�䆸l��-|�K��� �Y�sZ?>L-�y�	�+L�n����}u���z�Y.a�Z���}> +,��W��*�۷X�V%�5e��N�+8�ݮ�9��<z�[�y�HE��e�;�s|U�l�IÐ�ø�v4Y�'Os���c>�{�We"�{Л\{�k��*Gz���~����6�q���׍�w��S��O���~�e*��j��d�^�?�@9-�9s�z/���F�G�f��p��2/ �\*�#0V�F^���i��C��2Z�[9`vE;Pe����;�L�>iI��c�~t��`�@k��D�=
E�;`a�U*-NF�Zn���)�Eb+��瘋k�8����J�gO��UN�'�Zn�j��l��~mo�#�%`�2����+������:�X} �-���ӫ����|�W!U	��=�����a�Ay�?��sk��#!�4 y��8��(���YU�# ���X#[�����a�����m��Y<���������*����8gQ$�Xb�G��H�Pv)=����b}y�l�{�]�į��b'BU���~
7߃�������`�܋��/�/U[X�S{��b�"�1��<��I���/d
H��!�`���
8[����-�}��xC.� �h�{�h��s�ns�
��<M ���t�&�>���j�~�e����Xǯg5t�D+��j�vi�<�y��?�����d���}�\B��<��X#Z{΂�t�8lnp�뵎_X�>r+�Y�947	�sEz������/"SpaQ8�f�� iי�k'� �Vфz�y�%�y2v'8�x~T��O��羔m��/c�up{�������5��oS=2y��p�i*@��m&q������b�n��_�rf[3�����[�&���҅���|�;�$�&�s�����g�N��C9���}����Ñ�.6-g����s��J��z���e��(zz$Gz�ctN$?7_���ao����A�s��VD��5X��f��5[@qT�K��\h-V��#�i�d�זܻx�-Y߂4�פ?�'� ���F���<5�	03y��dˀ}��,�/[�D��scE1���:;X�������N:шI&\v�6�Y�&ȕ}�9d�ŹWw���w{�⑼���:	��H�]�ѐ]	�����Y��Nm|��4u(\���TL����%��h�Kళ����8�[�$�$��q,���kp���}��8��%\�vm�G/�ߝ�L��@����E �`�9b���*��0=�޳�(AF=/-�\�t��~�0Z��#��됮�(k������"�	}���/��Ld=���|'���H%�;i	ָ7>~���5F9��7J�$a:Z<	5Qҿ�$io�c�	{�M!����ɔ0K��r��5;��Ãnb3]��oݡ^Cr�G1���R@^Qdg�����-��8�r�V!���v*�Gv{�t��'���#�N���R�Z�1�j�)�	2����IZ|�.mr����b=��QM���(����'kSե������C��R��z7�;����C�_ݣ�W���oETu�(�^L�;$�ͩ��x�4�BW�|���xޙ2�8	`~�u� �Y1�s�<����#er�a]�(�����s���Y��:��@�PW�z�5ۄ�pN��7pE���M�!x�q9*K��cll(R���tQ�'o���9	��y>�;�����>L/d�Cc��g�,%(�ak��.`��\S�����QqJ��Y�8�����M��~$��B>eE�T�كgc�x'u+-p�H�0?)V�9Y4��޵N�i��!����0bl�,;��૴1��F�d[�o�O<Z=I��亄�A�x�T��4���8�Je5�� `�)���-\~8�-�4�ix1J�q&�+ѣ�i�a�v��K��;��`sw9�����D"E�6k����}H&�b�(�� .R�a�Af����7����7Z������%TJ�/��K���e��¹��!�Z ]6�j�CdW�����w�Q���Id=�}F�o��g�BX= ��U������i�M��X������e!F[���X����d?!�\�i�
C�Uݴ���zS���~����9�qdo�&Ƒ��Q&�!�@8�+3��������L�Mc��s#Hk�UԨMd�Dl�� �)����_V&b��Va�M�)��Gb�H*����
U�p'mK��{�2������^̉Zk�.=��q��!��*�� �[׼ۀI�a��l���3Tc+�>��DsӬ|�?���i1�x.Q{��N���"�V$ߨ���p0�4��ZIJ��ZL��������e�6Q&&��y��YZu!����IN�{�Qg��|�훒�U�&�zI'�uo"J����a�lo��Q��VçQ<1|n9�ؓu����5h�(�[�S� z8�wP�bo��a12@����i�<�Xw�q���t<�9�iߞ��Fb��<��*T���/�X�nhw
c��&�j����A�yOq�4 �S�gڭr?��n�q�H§e�~쪿�8J��V�<��Vs����Y@Z˻ YO�˦�,��CS&�ʟ���i�e����cεA�����SI'��cj,��\�n�gqahN�õ���R9�T��c_�xz2"�,x�Rg�O��u=G�l��<)�;�gg{���a��m�؅���F�#�5;Q�6���g�d���$�C�f]5���#<�L��g �S���ǯP�s��/6�M�v	���ǫ�ar�V��Ĳu����슥ㆨdZ�ѱ״��"�U�!|�<[B0��}`��E'A��>�ʑ����ᬧ�+G*^h}�m]�K�]�Tl1���
"v~�������Qya���x$~�V(�'��{ؿ���q��C�����Z/�甑��Y��. ik;�+Y8��H{9A��q-]�=�li����q����0/�n���Gޏ�x��(:�[������k�FJ�{7��x�#S'�n�ab�� ,h��|n �߈*fIQ渫G%��Vj%@��b
B6����0�����]�����L`sd�Ũ���M�r�B2��C ��0,����c3eAǩ�(�$ J�%!��	�hi�FW�qu4�Q�!���Fj9f��G�:�ã��F�k��}\D�����"c�N�#Q\�ՠ��>�ӓ�x/�U�Cc��c}.U��,G؁ŁY�d��c�) s!����1��2�oY���Cs�(b��@�Q3Ӡ��P��󾹳�T��:5��E���cپ�AL%�I��k7��3���e;4�FI=����%�b�!Ny�A��S8�u��?V$?�����9~�ZUN)��Q�,:��Tݔj{L��'�$?��%Ney�6������/%R�Q�����3�#����.揖�?�"I��bpgU �9O�J�{ֳ�ѐU�7y������ �;r�R�/��v��=QD|#ф�I���x�p���t��γ_�b�z1P+�,C?S;eBn=;����*�@����[����{�'S�P�rYix�8�'�R�v�%�b�nG�Κ/\y=�4t���)7I`	���$��'�?8�m4���X+���n<��B�����wY~ _�]*�C��ӣ{h؄�%�(ڤa�b��#����	lB���ު!���=*�L73^?�if��Erx���f�.^L��`N,̂�|ք盐��J�#O0�V�?�	���f�l���);2�mu�`���)�
�18����I���b>-��[�H�Ȧ�eO���z��1�&��w�������l���{Z��G�鰄\��O���Ѧ	@����s�/[2:ή��_�=>(�q��S@��l8����������YZ�:���o�#���K�Ồ��3'�>�t( 2ӏ���>W����92�-P�`���U$[��cY�jGo��x�y;�G�����7%-䣮�O.����Izہ:�Ү&A�!����j	`��b)kd�� �e���/�ؕuF�t�,�X�*zE.��z���c�{o��Yw5ъ�<��7U�K��x����U��r��8��ῐ���Dk�8h��6�`/�eܛ�[��<��G2��T���W ��H�O�t�U]�`84(�8m�&����p pmh$VM�$�	t�p���e�S��n>�k]P�|/��i'o��=��	�	�Su�.o���8��w!ŕ��Ws�Yx�RQAN�w�F.�҃�r��(�gKm	��F'3K��Fn�� GWs���y�U��C%QC�������?��-ɐ2]^ ~��� 䮑P� C���U�� ����	�������1tY�.����c�mB3��G�w&�^���<N����q�o5��L�_�b4�?��[��z�9ëk�wk�Lc+]o���{	,�����=�>�����4��v1'\ƴpݲTSOs�pNW��S�$&�w��n5bD>ةgr��N�-�<iQcV��������(�I>��6�ǈI������˥Tf?��Ml�۾h$L����3�D�W�iB���q���]$2}�����JWPe�=\	,7�MV��G��פ��O��ZT �Ȳ���Ѭ��#�E�� �P˱���FF�j���*YΞ���<� ��`��������@���. �����w�vM�Ťl�����;J��n[�/��/��{�L*MV�6�KH�Q��{5"n%0n!�v���:���+��7*�O��^���M:G��j�ͬ�����v�tq����/͠�ڧ:]����Rn
Scp�+��:<�B}`}[�';���k��ɠ	L1��W��?�|O�Q!$E>���Ɵwt*Lx ���2�������P����*�C�a�*{x�0��/�h�P	k�SS��8F�,&7��~��� �STZ�}�J3��U�Q�+5
�p�����������w��ѐ=�bȭh<���Mб�*Ke�O�-�TC;"(�(�����^���N&]F�[R���n�^N)s�b:|9�uǘ=��XQ�Ê^�S��$�'-Żo��M�`�?�K�s�<������7��5ߴ���XmP&��~pM:;;t/*�T�ì�a���{�l����PZL����9�����5��wǦ��Έi��t6zt�K~��Q�k���B���R��`s��Q5��[~�>�A�����$٨�nG�-�����O	��S�wN��έ�l?�Q�b��z�I�ւE�}�7��U�U��S���̒�ᷠyu&����j9�rkӒfiI�W�]�7��,TQ������-�@��m�w����^��2�A����v��x)��[����]����3m�?��:ґ�C��q�XC���s.ؤ��i�����5D��26��=>wR�C5y|JN��^�U��2�W��C#�Ė���Z�ׅ��i�BW@��.��߮���,�U�6�q��?���e��MˬH��	����2�6�A'�#��ԊWĬ�,Iq1!Y��NT��[�(��H}���N��d�\���R�}��0ɪ�]Z|�T���,Q~u[��������r�x>���n��V��q�8����g���]o%@��w+?Qcf2�wG��ƨ\iG/V����`���lDZ�ѬW���I�	�Ft�{�3�ڳ҈kOH�v�P�--��J+'��q�سzm��v���$1�����SN��._L�>���3a��
�����(ig�55���z�D�0v��g�g�����I�8��I���\$�ϴk͊��]8�Rtu m�@�fg����H���������9|МM�>nj��9���t=�$})�j���2*�}j|��l�A�9� `�E�������Ͼz)&��cΒd��,n��`s��.7Ԣ{{����|Cߓ�N[ J��=W��Na��M�{�]G�A���/ማi|����f�7A���@�\�$W��T�:��;cM����$�˂�;�W֝�@=Nb?���<��"РN���8��͘�<�3d9ɶ6�Gy-V�����i!��gx��۔ck�����<��1]sח�]�^�guZ&d�o���"�P�8^����=($8���ٍr�Tk��RY�Da���R�P�/?�zz�$%5 r�ͧ�qg4��K�����f��f?�����Е�=k�������|:����&O���WU�1־�`&�	;����dxN��6�ŉv�Q�����h�?���z%p�����C@64���Y]Vĵ�H�Xgꕬo��L��4̏Un1���?68�o'��o\I��?oŊ�&�ֻj���((�%��e=��d(ڕ�7/���`*��x"�p	g��1��5B�羂qI��~�n�&(��3$;�b�m�����x�T�y�A�ԽS�̯a�Y�ﰪ���ȦZ�ZɿBT�)~�<����\K@��y`Zbn��K6#�q-L^��O&`C��r�v/�.�Ǫ���e��������P����Y$$�%��_�N<M6�!���tM��A{�<������}�#�TDy���O�Lp�Z˕B��7L.d��� ����>W|���M� ,�����ؓ���oZt�&{S��y���Gz
�V;2_����Ky2�L�n��G���5mkH�L�����Z^%�|F8��
�5v����r0rA2�}�Y%�T�ZÂ��`�V3[���2�?9�#��Ѿ&�p�1G�zTE�D!�i��Gk��/v%c�YJ��oW�@.�g�{�I(��_L>h�u&arm�?Ll��_��׊�ļ�>m�yת�%�B�������cc���?t�[Z��~6�A(���q��08��R�&(���7P9W�����b�4�������{x\�$�aȸMV�t�=+�@����'z��39l�-](FF.p���`�Pm�ى�*���g<x^P��眵&> �����^j�L~�F�dj$lJ:��C� �$��i�����n�'Ru�朔Ѱ��ّ�ȝ���@��-�@��0���A!�{�gM��;ԋ��wh=�܍Ꟶ�V�덄>����F6� I��}�r^�U� �C�k�<�L~4{)xo��u)N��J?���	Q�����Ĳ��ƻۍ�myB�S�y��ǲ6?z��� ����g��*�'���&�_����9�c��N�D��9ZU*:�?7��(��dj�3��0�xR-��Z�J:����Yv�<6���T�Z¹�d��Ⱦ39:�Q��ۺ W0��6�N��B"BJ���z��v���*?�/Vb�+�|w(��}�R�e�f�F,��Ն;IlnK�9�)��E�^xޖG���fpQ��ˋ��$�~#��S�^e+�(Ac`6����rj�b���`Z��5·��!\�q֯FĪ,ed�{����5�Y�}
�����̊���^>�<-�&��y]=w]?��p�_�ӑ�DbI��;����`���K���Y폶��Iz:2�O��U8�p	/���ڡ�i���?�K|���vuW{Q�e!�E���~�'���E����v=���R9����&�w��o^�,;J���w!z3ߓ�XȨPt�K
H�#i�ַ��w�E��/ c�!z�M���/#%R�R�Ӎ���J�vq@m��
�`}i003������5H�#3�����/G�]����x��ؤ� <}F5o�^���c�IE�D��d�Y�>T�hS�{�]|��>,uUY��E<&:���m����ɱ�߁�9��}ˡ"Ξ�E>��݌[5#U)aZ �5��4�s�n��WJ�H�P���Q�6�m�l������1�O:�l�����i<F�����WX��DAhLw9��ޖQ(����J�>)=�!BA��9�Ku�^�[TJf��91�g�Y��R������� �o[m�>�}m����c�~�,�VeXL�3�����37�Ɖ���᛺��ƈ�F'yi˕`3�a�s=�/{~�х��H��f�B#�{�?]=%a$�
��������+�ִ�U;��+�Q��/v���M��*�I����4�VVo�.:x���/�������ޗa��\p�&h� f5æRn+�OcI'�DB�Zdtt�I�l>�i!n���;�?��m�(�W*�UU~�-U�F�A_�+د��0�H%_�+W�u"e�x�f\S�oG����j�WC2[��Xƅ�]�����&�p�Ũ0����c[ ���j�j�KTT����sJC��A���ܵ��5��U�&#5�'�zkl�ڪ��{�	�[Z6�.9��~Z`5'/¥��w'å�e�:޷ շ�����QN����s��y����J���~Ʈ�a|�8�.?�P.�UF;�5�,^oDȣ���`J�BȌ��/o�ZW��X��dY�yᰊ9W�IW<>6I�T���Q�&�DX��;�k^,�,�2��@� ��ކT� F�RN6��B��L���s�vu�u���73j��ȆԒ1��=P���D�蜽ޘ���!�~������E�����"��޿�}S���8���E�~������j+m:b���Ag������i�W7C��iES�2.t�hUS�EJ�������Q��Q\F�#lIx�/�!�}3��rZ����}]����%�L�-���x��rg��,��R?��(�٨�4�{����%i!D��C��cG�)�;wF;)�˾IMPB5�C���dts"WaU�c�%5)"�2�c4��C��$Y ���T$Ga*��{�]�����X?n_�qFr�����sI����]w������^�JT����]���G���h�5kc�\jD94�sN�d�$j�O�>8�!0v�U�=�M��;c(���n�N����W����̇�0�tfa%��\�?9��!�o;nN�@��LMi�����[߄�Z$ 9C�����9k�n���OK�ʆ�!Zk=+9�`t~@���;k� R�[EC���h:S}������M>��vV���)C��, hS��np�����`f]�f��{U龻^�b*�SHj��#`C5��5i�3�B�����g!%�@j�@�]??���dș]ƧN���^�ﳌ�@�wv䯗u��rs#tV��=�H�y���j����� �␪��*]n7+�&��Jj�������"TeEe��x����
�( ���G��	en��q,�9M�9�}ޜ*�sk:��$������|`������2�y�jG`UԪH�Wk�㸩d�饍�y5Э����/Ņ�={f��I��X<���Y�r��G��Ө�1U�-jp�]��%:x��1��S����Ϊ���1+����s�d��ޟY0O	�K�	=����k��OnK���څ����U^8ڪE����e��)Uہ�*���2Ѵ\\^�"�.}є��I�Q���ϯ���&��-�O��Ůtf��AD}��=�K��6f=��a�3m(�~��z�Z��"����E�	�}�Ip��~���U)v�1!q+<w,��C��g�~i�� ��A�GD˷�����xM����շ �vٿj2v��
5�����᠊qS���¸��^8�P���¹V4�ˠ�츓ń�FZt��t�������wI2|�z��0�e�)�K������s<�L����u<��<�\y6�Ժۑ��5��N��;71*�h��2��d����j�8�d,��D�H@ �zc9�� �j�!Ƭ�>y�	q�qJ�����j}�t\~��=7�z'e��Nb�Kȭf�o��I�����[��/e"UF���� $�2�d\�M��c�S׏@<����5��w}}%��s)qsw������G\M��kop�xV�\à�(Ћ;5m�Η��?׮kR8��XDf{�\�1^ڍ���_c�"�e6�2`C�Qf�ٯ+�NG��G�ߪͧ�9�3�����&&i��zi;��O9
�����{|��e�>�.T��� 8��>��E4�ቪ���xQ�'V��!;/���X�q�m�<���7��T��R�n���Cm
K1�ϊg�=x���B/��U>��7p�ge�h~�����_Af�p�����s��r��ɦ�vaxHr\b�;�����"/��}���.#N�6,�J"��_!��	e�R�?��]Vc]T]�=]q�m�T<(ξZ��KM~��E�t>@���!]�s�g^�&�-c5hzeq�޴.��.�hC���Ю
S�p݋��{�G~S��������p��`��L4\�Xρ�h��y|�T;�A���k8'Le3��
��w�j����K���u	O��)ߛt�	���G����`i���k;E_Y�#�7d���-6�{��uV���?�ظi����/��ۇ���A��2��
�~�%�����;��V��/"�n�Y�l���-�:��:3�;q&��Σu8���c\��4y��=Ǽ�F���վ��I��`����/Tr��b5���x�����FE1��"��wr-j4��aE:,������Yh58ھ�UFAr�V��Cde{,��]�MK��+����:��F��(&%��X5�ϡ��4���Mk��7b$�^=�ܔ8���Q�ٜ�qU9Z��{k���:�۬�қӃ�j[����_qJ_�:2����k�K_S����RpY�)�9T����A��*��s)`���1�7M���F�]����(��w�ܕ�Q�.� hØ���/[E�����:RɈ�����Q��C�D�j�J��究�����pm��b�v*i'z�W�*���m/>ٕ�?�hO��5���"F��ʘ)M�-��s��5��h`��Cw��$��*���r��F�@:�>�3��4���m� ��3�OF���C4�E��V�N2#Q��ٯZ�F�q��Y�J{��2�J�X(��1!=���R{
6����A<UR��+��-�h�p�z�K{�i]����9�2N�&�Wc�O�`���75�o���-ȑ�}z3�8`Ӥᣫ配]s^aF(��9)�eh�Τ�݂�5���i=&CeyF�*�l�/GpmW_ڢ����d��;��@���Q��s���L��3ܿ/Fm���[h��)�H����]���W>7ׯ��IC���#�h�Aǟ���bI�TvogB�i��06��4'5 U/2�<J�\�Y\1���sz�ǐ�4Ћ�M�x�>:��H�Jl��Z����V�&(O��-�g��Nܒ�j�G��� ^��wFr3��g�cwb�>���%2��<���8r(fÃ/g:�6��h�X`B�'еb3������U��MBlB=!��pV���Dx�@��=�Voo�ì�3O5�A�1Q5��<V�~�ʎ�G��n�ye��1H?�4���Z�����A����5џ8���G�u�s����^�@:ٴ)�h^��>ϏzQf=�����|�g�a��<åت�h�xGIldy'ԩL����©�g��	�$���OZ���<�@�΁���oT%�8��G/>��I~�ӧ`z�����t����㚤� ��i����t�ĒҤk6}������}3��k��̿�&������b�S4�57# K2���&ΥK7k�6i�����[��<L&��HQf��f�r�ί*!Gv/:�S~�5���kN���6�y��NÓ��m��3M�u�e������C�툂��e����|��;Wp�j<"x���e `���,=�5�y���v�����x���ߕ�$���Y��	4W��g4�kJ�͵�������h����&'X�}���7{���SD�����bv�st'�C���/�'�׷A���x�v+���΃'��&��FZB4e�:N�ۮ�g�'M^14oJ���	q9ߣ�0H�!eB��u\y�c+�]M�Y�������s�k�9�3�+�	o�n[�4����X.K���4�Ms����OW��n�X6��W�T�k�ܜy:�SS<�gW�<�|�zkz3�!��� 	M��bxa�c��D"�̴�(]��Ev��X������N�Yxy0s�8_	��U��`_t�Q{�a(��"�F�JH�c`��ef��6lt�S�(L�B���-q�
���2��/u�MW5">��͙��y�g�: �����{\U�.���޵'�������"UG��2���׎K�XU.�r�<2�i�V(͗#�"fQ�,jͰ�#�*89��2O��k+�l�w*��wUB�(ȁ�e7u�,���L�im���I��@����0h��ς �}WG���)3�ʏ�o�g�)W���M��ro�F��)��vz������є���
<�$\��/���U�K+U�8D�	c^͹�b��؆�d23���48X��&d��杸\f֙ܡP6�7"��ɯC�q��v7�R���Tpds ckET�V4]5���1b��6'qe�s3��.c�[�w��.~(-���#}@�@��l��� r��9��.���<o�tG��O#��TzE'z�."s�HPX���2��ƿc2u�s�g6<��}f~<�D���)���-{ʓ�*����:��H���n��Vz��!��Į{ϫp�	��=�ԏpcnǿ�M���f@�5�$��Egw���;k}c��I�>��BY1T��1��Yo�줼C����0,a7���eVx[Gn b�8���	��n�*Hλ,2Ęl��d�,_�Y��'�iw���$#�����8E�_�M=>@����4��;�U�&{Cz��R�(U�Ʃ����t?_'�KĬ^�X��1:���([�k��tX�������K�f�?G4Kѭ?���7�����}�<���=�����ȁ,!�3:g�!�m�9B�K?��X�����g�͚�͖�)�o-�G�"�.�6zH�B�`��愪�t.�b}����ca,��I~��;���:`۲O��۵ö�g|�0�U��i�����3\l3�K�V �6��. ��� �u�D<&7��-3���`jTђ��կI^Y\ʢn,؋�	]ɾ_ڃ_&�n�1�e$^����^���'�^��-��o`(n�ֈd��ǀ���vϑΓ)ߞH$�y��w�LiMЦ���1/'W�y�o���⺧��.�.҃���n�*��S���[����ޕ�Y�]0�#&����CG�2��$l0�L�"��v:K�mBλZ�R��Yp���*�����:H�KR�<?�F�e=���oV�A¦6�G���X����&��bm�{uG�8Sl�+5.�Xp�h�%������'�л4�v&���@��x��F�Lג�ă���B%��)n�-{�<��d�zpr�k"�6	�j<.��<73�ϊ����U�������&f��꞊����o��L�G���S$�����Dοʴ�Y#SQ C*=]� �{��K(3'��a�k[��],�Z�L�%<��|6�n��^"�ذ��Y��A[��!E/0m�B���z
_,@� ��ߩ_�"/� l_�j=);|��)��G�B� A|�uHǱCze}��������㈎��Z.B`,_"�nZ�#�{��Γ^�3b��hLmj���*IO2'�wV\@cGo��N�W�eO��S�+%]N6�֗>��w-�Dg8�<14"H���#�R�n�B��-�ހ�?!>��S�v��&��1\�^C���E���r@�k��>$�W�⺭�uWmΙ��͂�gCX��xO����m׀�bt:�QFwۍ��8�K��u�<Pг���H��.��Q�9����c)z����~��Ptu�m�&�{	��Cݠ_�����rx1,�M��Z�O��'M�d���M�F ��r>���C{�lǦ����G��ayY��>d���0���soJ�`�L�����S%�p�tyW��S�*К���Ů�$r�E�r�.�ǟ-���|EJ��hurY(���F�\�|�v;���6 z;evq�
k��#5Mu�!]y�W�ʻN���[��X^NT6�zLR����8�;��ӉF���1�~x��9�ɚ�$���f×�M�s��P7�P��B�Ӈ�Sघ{]����f	ஏ���[�*�E�ص���Cq$�L�so��9�S�~�W�.3�KW�Bs���ڏ:/h,���?�[3ىV�t*~>tc��j{����;�$��v���oZ�Z�%�LE�J߭���h�ar�����C��J�^ݒ=a�cY�?�ׂ���$O3=t�Z�]n|Y�f�� �S����x�yi�0��]J=�)�˃U�	��r�8�Q�/ez���*��G�(��UO�s
?����צvr��?��1�I���:+��@�}p�c�cb�� �ۆ�zP���L-94���㎅��Y.ȍ���lx�������z���`�-̊R�sٱ�Z�b����o�q?΂���D������ϯ~"�q#�I��L�����9���GzN��М���H�����C�k���$ ��y�B�	UĎF=�Q &�D�ntV���"�{�0�=f5���na���ok�@S�}�82[?��l��O��+z�����y��j�^�5O�pvb����臷ݑ������m�������Z��?%5}G�����?|J08H��_]�}�����Z��{*��)�&0dx}#����όlȰ񰮆]e��Y�� F,��R�@��X����]>e�$��Y(�o�G��&H<�˻�#p��8%s�5��6��kHɋG��ਔ������]-	�n��������)����m/w�~���9 ��w�8��0��aul[�o� ��=���pH����wB�����m�������g�}��{�����{�S5�2�o�k�`��FLﲶ��I��_b��� �!	�*B�hl��P�O�ǫ'��>���AW��4�=/$���
9ރb�v�������FnLag�]���)C��U{m�#���a j�»'�k��!���=Hm��k�V��G��j<�<�A:��|�C&�$�1�n�b���J_�P(l*=�����!������$�W�r�$�O��톅Q0E?�5|����G���6*L��T�)�1V>�������~���.���6OQ�Jf���X���gT��:LxEa��!��m��������`�U-J��tlgY*J��
3�N�~������������7�b�& 4�����LP��Oɗ��"7�� ���(3��-=M�MK����s?a~ҟ�p�d
�
��8k��`��~��5*Yɿ5uO<��l4'v�#u��P��ں�`�ē)�/��T�Y�|�/��Y��B-���˾���*(��2P��~1:��!��!:��iJw�sB��&�VA����Ӎ������#D�]��-�	Bc�^���7��	Xi���.!_��E$�0&��A�O`�/�ːp����iI�K�����hz��U��*I��*�����X��(S̜����VKV���Aߒ�թI$�ǈ��9��ܖ|����{Fd��V�gݷU`Em5���m7e�s�z�f�����ڣ�n��Ŵ����Z���Ň|;�c8�{�v2b3�S�ޭ��-�'��3���0���=>�H�R5�P��?��$�#�"bO}��(�"�3<�N�*w_#�7UB��Q��#�������C��ޤ���!l�R*|�r\`����d�|7k'�m��������*�.V>o-#�(�QH���X9GN�K����4�7��/
���?G�*m�����8«�{�)#}�],C� ����[ku��:IL��:�^����+gs5
h;���4�������\�L�b{U��Q�}�h@�\���)��ۓྃ�.6���W6���#�H�y�1b���������}�etk�vt�-��Iqa�B���G���d�-a�
2n�3u"�\�#��AD�Ӗ�AB~�AC��n�s�����f)�N��t2GO��I�T����-���+�	EVaI@��ץ��&�]�Ԇ�s+V�㌪��o���V%G$�Q�v��9�Fұ��m�5E��� 39��]*&r���Z�Fj~���ROު�*�A\E$};�!c�aQ��s[��+��I>O<*X�����nD���C�<]N�͝�4ٟ�Nbx\L5�8#{l�)�@�@��˟n�zU�;u���y ��fE��af+�YXf3�<�~T}T��j���9~���.����rƻ�݌���36�������8&�=�
&����9[�G������� ��îZWD���oM+��8��	���*�D�{`�=�H$�T��2S�,N9�ؗ���c�vOTА���� an�<dI�	�,���3�J]45tϸȲ%��i�2�|�S��p����	����	D�Ӯ�@Gx���vI�8+��H9s:�����p��c���A��.6P����.����CG.�"��d�2Oq4st��riɼ���Ç:�����=f_��@��g�����y&�9y�;�T���I��j5Tw\}�����LT�+t2_,-�kl���=��s9I�+��4Y�O|QړgU����:�r����%�];��J'͛m�zF�ZB<wo��,��Jāf�Tw;�'VO> ��,t1o��E�t]���@�a7���+h$��oT����##�Nî��k�RN��s@$��W�ܖ˨;Ԉ�;,��T�
4㲊�a��`�g	��GR; ~$�R�sSb|#&UJ�Ӷ�a���":Y�;TE5�hf6�9�d��|o~����ĩ���1�p��(��{p�/� �ȱ�bi�2`�}P�	��	 x)d����_^mV��wӟ'�����N��V�����Xf7��&X��%BtCj��T�}D��6��>R������di���lR��8r��=<�f�h;Iлx݁j����K���v���}-�oA�
|�"c��� -��p_~A�����`�Ve�rn�B�&㳅 	��,�/W�PdyɄнm������]C.�_ja�w�-�&ϰ��`�8��Ӣ�,b��h���^.P̜��5�+7��!�E<�oU?CE�_�c^_�(�-�o�Q��v�u�u�ݦf���?�HKWs�0>ܺ �����Egɉ�v\�=�+����&�Vb��Y%�$X���5����,#7����p�yٜ6��+�5G3�9��o;�C'	�͐M�Y-&U�چA��.��/Q/�-�$�`.h��xJEg����Lヺ�cՑLo]���ϯ���ц��N�#j���<��f�6	��Hv����Rj_)]�`�:��*�\����d6�;�q�����&�*�#�z"6�+1�g�YdQǮ�{}���B)��=�U���_� ��G�8�k4� �`G�엖��P�O��Sl�t�Ֆ��<�Bu�� "B�-�����3�S���Y.��T���H)��z����V������Y�K;��b��,�֨n��S� ��ΪV�����������X��_+�,� �Ǎ1�X֟Ǯ��q�rg��Xz/�Q��D�������ɿ���(h��Z��'CT����7$���Q&5��y"�4� �V_ ����"�Ֆ����감��⭱�p�OXv*�������ݘ�:�NJ�9	x����]TP"uo�U%t#�|����SJ�*VWĐ�k�_�D��5�?��0����O�/y���Qq&�	=h�!� ���>k��qL�� �`��Y��
��h�M��RI��K�B��3��֋İ�A|�v+��ӥ�vO��7;�~���c��l����	2�X��%�moWf�C?�}�Z��:��{�0�`~����j�� ��
km�����m¥Q2���"*��5�s%�즰%��iô���[�j�i�;b��!�"���Z����~�gG�|���|œ��N�=�|+�U�Q�]/<S-S��30Er%���KMA'�.��&c�1p�nu%�KW:�y�N)��Q�b�kVt>�t��\��S��GUF�ɇPA7�<��!��fݏ���M�qEoP$(�5@1Nr����g�gX���ِ-���2���ҁ���+�.0D�Wn�{�;���&�`�����!�	|��U�D��f�S�m���8h����
�c�͆x ��w��KK8VŜ�l��6Y`�
_�����F�M����ˁ)�����zA�eڦ�Ǳ�Ǹ���if�Aӣg��t+#=�O�=dv��&��ԣJ��G̋�4��F�{�����i��g���mH��Pa����ҩ4��
M���)˟��f��LhB�j�|�k��(t�n�ש�6�]%���������΅A��ϾȇCE�il�gy��Oax��
Z�YM��"<c�Û/��#�Y.��E���URm���閕���CQ��������#��_[�.[|,z8&g�;Y����y��OGżx ������B������wޞ�N`���z�G��uY$W?�@,�p�ȿ�q���{lW��9��g��5�I�ϋr���C����n �|tȌ�{�Q0�s��da�vb�%��.�J_cm���C��ݭl
aW8Zo�i�o�f΄a*���5���=�,�ꭨ~R�C�Q��l������lᎷG��\�Z�x�̭*��\�C�<�˶,ܐ�<f0�O�q�oN�D`��<��ĵ�m9_��̙s> R���vR"w.���/��46��'Ϣ`���:�^z�h�-�<pǒӓ���u�8�.�{P� �˓�C�v5_O�u����XFޯ�햂�~~i�2��)gP����p>a������S����0BO$d�85��k>����.ZR]~):Z4� n�q�ܻ��|�l�Jߴ�`�3�����+�Fz!���pwc�"��G1�ጅ?��ӎ�藿�H�	<�`�k�h/
����
/ʃ*1�].�TͷE����.�^l���2
���[�[ܚ�ׅ��Gj��
f͍���T*��j밖2LX
�pTBS�'׵��O��Ą�����z��~ŀ��f'�W�������0�
��x��U`v�jU=*F�������|6a.�����^:N�o( �4���!�O��-@:�g��ܷ��*�>qqi��[� �mj�4�����aZ�3�z&e�wT�3'l�J"~d1<�@�H�l��f�m�/n�������i��kɆ������B���ve������5!��0`�+��F�%��k0'C|�v��O��4�]A-�݇���uT�8j�X�M�\���wi{�2_�P'��ܯl�����l���Ñ>�}�Y��U[�Tq`l{0�
���	���V��g+v'u񥾒��	�z�'��(A��SO�|��$��`U�r-f=�J��'nj�/�iei��M�#�0�z�t�&Z����8Z�1�����<��U���	Ķ]����z�U[��y��	�<�@Db���{�щΑe��%#�.w4��n�iK
ZUb��=߯��S�4	V����~}�:8�7�d,V��(
wM�'�������ٲ��$���M�Ӎ�!��>��{^5���\b�q���ay���"
g�T�XI��V�m5~*kt�����Q���g+���~�aR.;�cU���⽩��f2��׹`�����lCA�7�F����_��c�;ɀ�0�%&
@ĥk{��!�lNz#�蔺��?�W5�\ź
���|o�$�	2E��>�A��; �
����v.�fn��u�B_Z�H����/���.��K'	�3��%(2���V`�m�9��_Y�~� '!<c!c��¨�`�P=
vU���l��M���uݫ�4)�z|uo����Q���L8
��"��6V����󱉩�!��ޫ9��i���m��6�f�m����c
�U3� ��W�y��G����S:�[ᛁ�D�0|��.�?���	X�V�By����F�-��;W���u�H�)��5�\�DW������������}w�)Y�V
��:��з���+������]�:�Nu��j���#�Z�`i}"�u�d��ž�����c?]&��#j1S3؝�#���������4�+�=�r~�`эb�L�@�����YJ���չ�[���^��~�v���e���a/w���5o�Z�-򿵚?A�L�t^A��7�69�o&3��w�B�D�5�C�Ch��Fz��O$��+��a������{��d��y�Ҁ���g�F�J���-)C����ݢ�����qDZ+�_{K<p�$$'�7��K=B����ݰn�O�6A����_P��G{����!�zk����q���i�#yڃ����FX=�c�Z��`ޘ^׫#�TJ��|�j�8I���<b�M�'��	:c��P��[���������&VA�Kj�
�M&���h*��N��1�h|V�͞�W���e3��&bJ]=����ߖu��!��ο�&}Mm�T��n�#���>uZ�к>#��]�t���u���C[Ĭ�:�R�J�.8��[�ԁ���Fֺm�J'� n��}c�"��WI;�8~�>�N�U���a��:� ��u��K'�I������a��ݬ X�{X���k>'�Q��GJn[�����ʗ��q6��i=��79�~d}�>���
>�xs1R�8��?,NR���k�]؟M�C�o���ij=< ����l=ik]��p;�%e*�ey��_����=;܂�T�p�	(i'���~����H䅼w�]��y���h���Z ~���L��n�&0s]��0��Q���"=�J����T���s�,����B~�L|<W��`A'��.ђkri?�7����v����kU��s�X��<���"(�y��k�[�R�H�����C&��Uv�]kJvYRV�UV<�4@(DD�fF��r�4y����5G���͎$ن�]F����;���̜ `N����\�&���^�vM6��9Z�,��w���n,6��x�R6�r>���� 4��>�'���ǈb��
/f��x�8g�??��v�D���p[mQ��=�����F������D�t��K�簿e�̅n�ʛ�@��5�^�ZGöws0�������$!�I�Q3܍y�&����s���4h�xq�I���	���O�M��3��F��E���( a��MM)�O���Rs+�V�4�6q��t#P|{��qL~�f�++���7����i�]y��MsS�a�5��׼��%��z��>�2�%��NX��|\�q˥QjC1_��Y��T�Z9�n��[�t_(�+U��Ӕ�?v;�g�]}1���>�� 8ڽt��w8�v��%}��ؽ����	G��9a�;�!6��-B�t������A���Cq���/��&��f.���i$3�9u�ǟ,�/�+E�{��`�p43ʏ��%�3�>�����w�N>E�Ȫai)�v�I��x��7՘��>�Ą�
f)~�BNS�%N��;M�Ȣ�F�ߗ�������9�|?^�*5�y�@�m:��m�:��Ę���B��Bƭu����R��;=f۵ir*R�=�4�}��g>$Q�任u�����Tԑ�Z��OE��d� ���b��-{�ƹ7��~�����֚�Av�1N�a�b��@����Sn��Q����kL[�}�Ul���Ed�u�������n���0���0=o/�4��ip9������=�ܟ%�s֠��ݽ��C�ץ6/����_6P{������~��$���n�>�7��t�*�2_���e/�L눍�p5M.D����u���Q:}������L�8Ve O�M���@�Y�$fhG�"����sl�0����_��­�=):�0�F��3���D�ބ~e�~�����gћ��Xs�{�� H7$ˀr%����8{+!|
o_X��r�j�91̄�3�����(�sQ[� �S�"����(:�����D�^���N�����)��i��X�10-(b-}��i�F�FR�O�!�q�K�d@�v�@c��+��(z�~���ۍ�:����7欫���mHZ	���KXŊ*� ���<��([N��������f��UT0Zi$7������V߾���^v՟�p��*�[u�W�zr� � �.�H\Y���>�9NU �j����l����ݏSQ�0�G��^~�sޯ�+c`�p���q�8ϳR�ׅpo�Y�/��ɦc��z8B��UQ���}GO/�T��W�����#s��P���g�~4(�<�d=8Da?�x����G��@�#�����y��C6v�h�h9K�����7ݝ{ۧb�T����v$0 �'Gmk�mȳ f?2���O^���oА�z�)�w���
�y�-8��doُb�+�-���u�r ے�7h"YQ6�5g�_��ݳ5JN3�M=m<?n�����ž���T�%׀ Rw�z�eT��mYR��3t-E,�\0`y��@pN�@��Cϻt�a�1N�q��W�M�����(�o��+R|�?8���YK�,2��r�Y ��d-K�Wn2YY�P�>O`��:w��x�� >;""o�Y�*����Y�{j����_w�*c�x=�#]2+�2�L#��h,Ժ�zP�=�:Sԑ׆��5�B��d�}D����˸�?��4 �������c�w�}�F�T4�(6.
�K�H�5���>�K����чI���C��Cg���\�jS�1�10��
W�q��������A�wֳ�@� t�k����M$f�s�C�D�U���O$@j�#�_�B�@!\�'Ÿ�x�Z�f����~of����M�L9�Z�7BK��e��VD�nS_iB�+�k[九��@�sa�;~��ۻv���u�zw�;���6KrՕF��?�ǦʈRؗt~����i"� �Y�����}; ��vm�A��e�[깳�X���@���k����l!��Y�+���"�H�~g��t�M�$o�Lɶs�|�� q޵t���+� ��H9Q�-�S�3����ә��s�����Q��Jki�`��ײ9�Բ�HBZ<R�F�\����Lo|,_YI;�n1����k���3~�gqc5>�J{���5�|g�����M��cBS��u(W�	���2���������dv3m�@�^V.{�8��v����ꏂ4_��|&����Q~w�}u&�m��庤r�H�Lə�g~�H�R��s�����W{5W���
�W��S���e�#�8�I�]�v�i\��J�x36R�_`�Vm�<v�q�(.�m{�/����|�U%I���#n/�C^��O�6%��Ы��-8�2�r���rE,��`ɜ�F4�=+��*��I���E2���H�}���Fԓ�'?3�f�>�F���3��K4��r���QPU�qg�}���~�m���V�-��1��}�Hu�R���k����oV�~�UC�Dt���t���_mxh���$+9U.���<	�w)�pXms~B���5c]�1�C��㺎˓�+���'_/II�^���}���	�tc\���s\޼F �=���J�=w�2HT��N�s�'�ޠƷߣ�V60@2VLs!�gI������C�!ﲯ x�
}��T�ZO?���x��{�Oל�)���v���>����c��p��i�h�D�oq]p/a��0^�Xi��k�Q{zZeYdW���z����
	=����\�����WzS��)K7}1�x�qu�Q�H���@�)���nϺ��F jΖ�ʷԓD�9�?�hRQ�x@�]bk>�?�Uonl�xE'�Z���'�w��p�JO�w��aoE�;�{w��"%Y��Ē�2eS������~ADO2��`3�HI�*����)�:v]����S;>�]}�=��Iw���	�(Mj&JX���Js~[.��G^Uي�W%jar��P����P�/引��q����x�u��_/���aM��LE�@D� )kڅmr�0Pe��X��g�J\��-C2��y��{4vi��QO�U[���19j�G��(ӓ�n�:z� �Q`�w�j2L�]�/���������x�
�악l���l�ܡ}(ե
��n�G��f�,�/��!��,��j]G�.��'��v/���B�\&>=�t
�z�/�ō"&"o>anP/��pϚaZD���x������5o��DBh!���969'�:u������L#��x$�� ��@$�KiZ�5G~ytg�Of��D�ӣC��	\����������@�	ҵ��y����D�������_�a��:Z�'Q9܍�����䇊T0p�
�X�g�g�(�Is4L-í5� �#�~�g΃��/'��;4Wg%��4����[R)�%�[^���`��"�Ƞ������ˁ�#���[uúOI~�t�d!�&O1�5�9yG¯�%$k�{�7�[��K0/��}�ÔF��%�0��A$��9�AL�t;|u�R4Y���L@������
�`�����L���LE����qhQ�S��u�֕��xۦ%I!���Oį�hO=�'&[Qr���TE�/���]b��1Q��I�}A��[���;\i�5�x@��U�V�]�{�o^���7�(�[H���Ჟs#��s�5b�WƤ�9�~�*�_ħ�5�q�w;�7�璤^��,�S(�qL0`�2/�`^�����eJ�߄w!}b��n~�a>d�v�n3d�<������q=�]�h�ւX�?�İ���A�݁d����e�7`�]�P�0�[�dA�k���A�u�������~�0�k}G�/]cǷ��\�ɑ�RT��������<��o�#>F80��wk�fx�$߯�BĈ��yTId��ܪ.�n��z^ ����6�{�_)�0Ҭ�a����+��+X�\��T�� ,ϭ�w�~��?J���v<ݤr�`�aJ�zM�v�5X�3Q&���ң�����"@�#Q ��	k<�L���H�R/�M�]�{��f�����:o��nϑm���7��
����Q?���*,���U�-q�m]'�`�Y�H�t�ҵ��ח��᳢k �P�P����(B��?�����k���e~~!cVUt״�lE�-����)��t>I1�bT�����j��ԫ�z�og��G�l I�4w?��Rv�C\���9J��S�8
/R-|z����Wǅ���R�%$��/�-�έ�5z��^-| !?
k�2x�k��G�G�5}��/�3�=�1�ݬ�oil.儎 5w�)=��Y0{��Jĥ�#����$T���\�H��/�;��_����:��ҽL���^�+R���|,����&3Ʊw����ьR�8+!rq�����YAG`X�`�/+�"����I2��x��}��]�ow�����y*��_��4i��<�d��5��A13��(�IS�X#��/,	D�y)P�`)Z{W�H�i;���/��R	��0�ط�Z�d ����
lr#@����~<r���G��Dz��w�p��R����h����`O�[[<�\���!!����[��e���� E(�:sf�7���.����X�wաH�&8#��Fu�t�)�r`�P���������/r��+7�Zq��9D��7�>'��3ͭ��2�۱Q#
훡K�����,��B��w�>,1H {8CF���rwY��|��N�����g������F�42+>klD·ۨ�����]�Y�m��uC
v~�-p�Y�T(�㓑Yp��6~����-E����[�����_�ItN�1�1���G^��� ��ۦ�����D�k����{�o���U�V%&]^]�"DQ�nl�� ��鈏�]��m����9!�d���@\�n�D��|�����Lt����0��5�~��Ưk9�it�OU��M�gM;��t�G��+��Wj�j��
U���?Sx�I��*��c�dV_љo���Y�㏧U?�%������t�|`��4A��7j=W�WL^6&�m�Q�*��
z?��sn62��e^xp�3��1U#R�n68���T��ݒ�PH��4���17�̚�̒"0Ԓ�H(�Ϋ)��٣+�yb�k��/�vn�kG1>��W�Dp� ��H�hA�<¸6E��{BL?���DkOBԪP���h���ߨ��@�;vc��������[���,��{ʹq����'
��*�������4+"C�vPU]����^����ҵ�QcPe�K��kk_j�i����!�XR�w	�H�X�E5�ݥ0?���('y��u��`I54(fR�%�_qz�6yQȎ�:Ė&������)m��&����D��s���_����-���w�3ïӘ����:�?�6a2����U'~o�����d�fpw ��@��GފN�o(3̘/��%����L�s��(���{b��)=�M�DM\��baݠ�\�ؠ'&D���zD͹����ܨ��(�z�c�xk>NîP�!�[�A�	~���%�	M�'�N��s�n��V���U�?���P���97R�ل�m�"��s�>�����!���3�k��+ �Im@k�qk�|��p������=+�#V�v9rHT� ������R�݊L���9��)F�/�v����"�ů�y��G�dIWڙ��������Q��R��F�*�C�E�B
ay������ �̽�n�>E�'!C�f�#�=��/	��+\�&9z���nݰ�4҇��io~�k���Mq�~qå��M���"��kH�Ъ:F���3��
a"�;ܘ��$G4#KS#���ۗ1��t/�m� |�P-"jw3?.�#�V��������}_�8IP�@�`��<���K���=���X�;��}wd�oƗ���/�Z0S_\�`�-��x�X���ɵݜ݃go�<�&|{�G[���՝�?�i�7h?�7�G Õ��΅@�'��s93VgO&����]gњ@��R�d��b�m>��{�y/����J�OM3kR����ӑ�G�&��*d-��}��<U�[��Y�g��M���˺�	�7�f[��3RX��v�hr���e�/mþ���Q��eI�2�h�S�E�U�;��LiƐ��e���|������@ٵ��~6����{�4����E��c�HwG�ǟ�yu���ɰ�N�Q)���,���o'ʕ0j��ɴ8J�I��P9�`K2wɎ3ug�,bz��=ݻ��#!0{���w�2���5����E��VBl��!Ck6,��+)-�ǳ�Sױ��͏1��sB#�M�WM�*�,����mW;VI�Fɴ��O��Ў���D��
��y3;�"ss�5ْ_�O��񭪲��!�2�3����cdo(�cy�Vyr�0[L	o�r!�S�a�-ZAJ�^�P"��uǔ�~7�{��1���"Z�w���c�Y<�=������?�ML�gݮ-���$�����MX�u90�vQ�����·;��N��N��Z�g>F��Y�,0c��a|O����3���ݔp��e�r�0"����h<h˱J#Qi�p�^�r�Q� ��$����ۍ�"��B��~H��FwX��)Ir��*��S#�3}�ۘ	^�`���
�&�O�R��ף����D���&�M0��uz��HT�9n��27�z�Ll�>��<�!YA��Q��&s*m��|��W��MM�=ðOyxg�DԂH��ױ��Su#ſ^c�_9��bǏ��`�("@�?}D,kR�7{�^��_���N���<z���-��l��p�[��cM4]������&�t�^0��Q{�x>S�Z6�F���G���������ԋ�����i�,8@����C�P��r���H�ܤQ��}����Ӣ%F(}O� � 000�ԪR0�q�_�����u��9[9P���VX��`�����Y7<�����>Xau)�3�^��M^i?͏�ao��kѰ^��Xk�����z�E\*rG�re/����B�Km{bZ���Ň���M��B��wt�;��R�-��0��,�g�I�ZIlK,sp ���qm��Q̛�C����nlO��$�,ǃxc���H[1DIn�>~L�����`w��/��kU0ε|�L����4	b�Țx4�ӚM�M.l`�����Ur�qZ�a�J��Ua���b���{y���9b�a6�`�;n;x;*��z���d�#�?��{E]_�������o�4KI:˫�	�� F���;��\?�BV����am,�\a'�$n���<�td����^A~8�aqS(��3K��h����M��=*����:����ʰ��DY�k}��f̸Z+���_oP$�>�ץ4��R��x5b:!:��7Σ��
�c45�����,xa����h�~:1��[��gx�_	xR��j0dIYh�UJʖ�Q��D24�+��O/�S.\΁QN�|�Eth7�9�e}x�Eڝ�t�����;.bݗ�\�@�~#�CC�%qD�o��������,�$�n� �{^�N�%=�៤LѦ
$��@�D�ٷ�����bYb�#���C������!!��LK��L����P�&o{S���t�(�{9m���ݖ�������%�H�k���kv�l�����_��
�t�-��Gl"#Ӭ�&��S�"�5�!6�v\�d%���O���s_��c����≁@`"��ϴ��TD%ͯ�g��ĕ�&)1���X��9墒���O���o���v�q@J7i+�A�o3S�R�~V�Z�nw�M��J
%�i뙛�cb���{��Y�ڐu�jMg�ҝ._W�r�u[�S�Tڅ|U	<�]$b�o��y�nڬ�)�ص��R�;��x�0�G(F����z��-�����'��q�H�i�f��M�U�Qr�H[�O�� ��P��\^���/ޫ\M��J�I�7���,|� (�LE�*X�"y��P�FmKou=�EE�����x����əb�T�K*w.	%Tty˜���f4Iς=���N�����&�%'�VN"P�`����֜�7Ӊ��8	s����j��
�GuU�t�������V�6�I��<�t>���v���������E������M2�AA~ZJ��ao&B��!��*���_�'jy�����f	L۩m�f��*�z&DD�(K\%#2��Os�7>����*���f ��R�Ŗ�S����m�t�D|Ź�lGǐ���){����$���]BFE��r;�hD|W�����ug#�4UY�69���X�e���5�ϡ�#���S.B�#�>2�X��9��x�`*�q���Z�5�G����>|H�:L��_؈��v{"+ir\A�'��'��^P�*���.s�^��`k~�r4�=T�Ϭ��Ŋ�%%��CP��_��%u��>�Q'?�v��&���7�������*���vqs��2�FFL����l@��Sۗf��ŏ-�x�λ��r4þuz�o�$�s�A����-�1}n����&�C2@:��M��9�S�/�/��r0�Z&��4B����aU�ؖ���b���G��U^���ČӶ�YF]���p�c>E'�*�|���9}"�T��b�ڧ?iD�F����P��Л��	�~6�U(�-��'w�z=�(:q����f���X�a|�*^G;c��k����͊V��%��hv��S�~J��@��P�tv;����	���w�i�{�ɯ^P�{t�@�F�'����K��F����٫1�l�Lv��ę́%D=�:���46x>U���+�����e{ L��P0�Ǘ|�cC�������!L)��B�.��-��V���U��`�RL�� �h�C��w��k(��R���F��AKE6�98P��_rP��g�����\VZ�� �*�l㈖�F���{�C���>�G�^��c7�����{�����=���+���ٰ���aٟ`я|��H���ڮQ��M��\�|��Y)%+��w%�O����;�;�L�+�h�!}SF��oH��l�=�2�	��#A2?�\0=�]��w�{ܝnXV@ߩ��db��z��cS�u-�5�:^��>��7ˡ���_��o�1-cE	Rpe
�p<�� �ݺn�ST�._R��b��/�l}U�����-�����9�`?�˩�Jm�Y	�Z5�Mk�65�4>T����C%��.�^���݃ゔ�S�>�*�W�Xow���q`N���|&�[TQ/��cnuө=�%Z+5�������y�]�N���P��U�+Z8��Ȍ��}���V֪��2�>:T�%7����Ah�L�ս�fs��5g0I�;ah������'��e9�),|z]7J��Sv<W劫�V��O��ZS� |�;=��b�ss�$�9�j$�:�#q8��lJ�뎆��v/|G�im�|� ���[uOHh����А���;�u��I�Wpf����T���oo�O�c]�9ˬN�m�(�Q�p���h��N�{�:�H�?�)~5�_���tu��:�����
C�#5��z�o�.o��Vo�zn���kr�)���h���pl#���L�S�'�H]amCҕcA�{"�<퇱:��Tzan�֢*����h�KL������~g�;o���7��O�w�Z����jiь�	F��Ӣ���e��L�o�J*�y+�%2C��ֻ�$]U����x�P�ޓ�H#�>��<��s8�ػ8���wiO�%,���v�ؚ�H��9I���Z<l����F� ���lQS�~m��ZCP���κ��׽FG�΀�\��T4v���"��ѵK����eF�S& ����;$�${l�j���4gv�SPD��iJ�%z7�
����v�#��s��U�Qó���ڪmMm� c����*�p�z�T�����1!��α[���e�+&l��
݅sVl"1r�+�+G��PW�6����\�E�e�*7NX���~CD���C���/B�E&�vm�~T�{?/�myÑ��*�8����P'�/�s�D�ҽ���x>s'set&̎{�ޜ�o�;�"�ܻA'�O"�z��?����k>�fJ��G~��YL���R�%�6������]�jϬK����2��CEJ��X��R�-�66>�V����A̖=܌XI9�۷M(��];S�Kaء�����ۛwGw+�G����'B��µs ������HuAX��o�ǹ�ht����~�{�w�P��'��[���ʗd�@�Qۚ�!g�L�?Tf42A��iZ��Vw��A���=�Z'�s��Р����v�-^d"3���E�G�򴈤E����ޣj����1p{g�T�؛��w3��+h�y�r])�Q����u���������cI�v-����bf�,fff���,fffF��%�Y[�����p���Y�3�߽s�?w�\U�;�͈x����^yj|�������No
�A�o�u�,x\�-~ߓ��/n�A\D7� w}D�����)�2JZ��:���>��K�����_:�Ç����Yy6� -4���a��.�i-(���sF����\�ϝ���
K34��K��9Xk��@�㌟H�.xf5��:�?^!���F�Z�C�N��.��_pʭW?���'��*��n	z8&?5��ϱ�u�w�jϻFB8��D�"5���c��;�?�$��)�.�u6s��1���%_2R���5��k������v�����` �5b ��"���+��7����S���Eg^a<��~��)�_�E���ҽ�A��0�zsG��A	.CQ!м��U������	�,���=���U:��^#N}�R��n������-��*����[��j��`�
"*�Z��⍪�b��_���m�^��,��o�~|[�y��B�O�k8e�s��y�Its���5
C��݁�p�3��%��9��p���V\Į@�WW���3�4� >JǋuQ��F���v}ǋ������I����ZD�b����������3Y�x0�l7������ϸ�8Ӎ+�T as]v��o�)��� ף���!�7�Y
v*������!����J$�.jfT�d���ļY
���i"ڄ�����a��t�����Xn�A�K�=�;�눊W���d�,�x\�L��=5@lN/�M�\�	OĴ2�t0>0�	n���od`2���洪��rǔ�t?������c��/.FkA*��q�pđ�ruу��<�� 
ۍ�fDR�ι��;���}��{��>�V���j>�L�.kT��?�ʓD�4�6�x1@�����b��G/=�~`�xm��mjwf�L��.k�����-�'�Վ�G����٧lj�S�D��Ì/ϿD���.[�����Y��i�>�]C�迅]y}Z�%��m��.�K�\�zpb����)��6I9��3uMEdOC�`,�Lq�c.c��s��wf�48z4�9�,*X/c�I)_7,��?!z!ק"7<�����^�=��՛��f���	p�j{���{?�A.�p��^:��/�=��Yw�_��\�M�����0��!�H|�(��?�M�bH7��'�3�	��W����2+��5��}y
�D�9J��rJ]��sMF�3z��yٿ6���s�q^6ʼ+Lat\ρD%�{�b|5�v��⾾<��b��_a���/���W�b��� =��ӂ��`ݿd��� �����ʞY�C��ɑƑ����2]��m������ɏ���\ǭn��tAM�B��
%ީ&l�l��S���RƭW��>7s,����ߡ.�e�=wӇ�Em���'z��^��q�6�~2PA�j�މ�{M��6�����싡�?�!'��E�q5ح�?��<x�:����h��M�e<���P�ƛE�b/t����Bw)f8Z���u<��5���H�?GI�za�`���\��C���?,ě�A��e��H�N6�߽�=V�t�}�;�M��;��`�R�a�����D|4:���m��� pk����v�	.֘�*4^��'��ǡ2~gK����[�y%i��ݼ�e�-�娫M*̧u���q����O���q�B��[k8�h�e�ܽ����~fsi��3�U�
C�+�5�3�x�r9��fE��}��I8J�	>��,�*�c �����x��\�ab��R{2���A�2�j���ٻ��V)ٛ���og��.���x�t��"����dB=��{]u�g�O���1B��)?�یa����f
�(8�UI`�j�k�H�C ( 6�M?���d�P�_R=�A�D�����գ��T�أ	C�ܡM�r����:f�\	8���|���b�� b���V�c���j�-��~?�㾌�GNBw ?�����/j2hu� ������U�+I;~3��p5'm�Kdp��<��dw>��@�N�ҊSWwlϺ�m������Z�Mބ�	f������������ �U��V̝��ꎋ��������K�Ŋ��JU��2-t�u�j����_�6eD�`$�67o��I::M��f�Ns�~ֈ=d�J3��Q����@�U\Y�3A������v�zXg5�6��N�3��ho��N���Jl�'<ɽ+S���G��M�!��I*^0�C���B[����%L�`t�24�������%�������h��� OZ��g䈼[�=�,I6,��[&���rD��
�Y�ֶ�/9�T`��.
wH�	J����n��5(��\����[��P�z�uDb�C�|�R"��[붉�����_�T¸w�Q�7�Or�U�4��"F��A�<��i�Yh�_�͎i��=Ɖyq��� Ʋ������J�Y����U+�d�OȦ-�K��w�B��SR�/��������C�s���oQ���I���U��-\��IrQ�	ț����7��2���G�K�0J�vګ�>�S�����U�䠾�UY����l�/�O�dmTZ�Ļг���&EF�z_F�X�|{t��ұ4����-V�ߤu�[�!������:��h��8��##��<���uDU�m�s��;�9��[�!��4�=�����X�Ƥ!/���:a
�<i꒾�}��19�#��j���X���Bz�#Q?un�������z����W�V��X��0�#E�=��G��
T�ӧc��p�0%;��q��[:�Y��xy�����bD"�W[˛c�8�mz�jH�}gϐ����R�>iY�T1T��sۍ%fX�!�Ms�̎�*α)b�r"�w a����/�6�Ɉ���)}`M��_�d�n9o�i��TW�|�Jt�9�8u���?������KW��	X3��e�&]�.��j��|�J�����`(�=�T�	UPdg��5���e�|��D7S5F��zS�3��8r2:�톿}��Ǭ���ΐe�=l/����I�~,�[p�Ô���z+�W�@��?�q�ĭ��j�\�[���S�%�+�b?��0$�@!"�J�!�.�VF�RB�����/A��Y�J� ����u�	+,�y`���Yi�{���mB��d����/��JE�1^ʿ_ �wD��ϣ��dC��|���*367jU��w!����k	����HdV�j�$��[@C�H��}g�)��ㅝ�1Y���ZI I�;o����r��3�^�tڅ�zb��mC'��\uX~�E�>E�Qг�N	� O8��z�"��=�Þ҄.�<���`Д8�ډ_9�-Eda�z]`rBDs��BoD��x��w疝�v��DA�+KoJ�/e7�d���y� @���Ͼ�MW�^�ޠ��('Ri��JS�@��)��C��K���dO�?�r8~��p8(��k���m�Գ6+&�H�����7���8jݽ��~i�扉촯E�0�Z%���dz�p��f��Fl�4���E�ҡ����yU��'�XY�#�G�G]$�]���ko��犾�{�-W�u+�sb��B�7�����(���_M�ڙ��Q���R�-z1���g�:�����y碪U�`a����(�8����\h�͖��`�	-h|!mK����c�������~�AM������
�Qhp�O	X�Шr���n�a!�qhs�S#m�yYr��a�����9%�JV��T�5y]fͅ�$x�md;��pJ�Ї��/�:P(>f�+��>��o��рq��/��!qX�!S�	�2BI�F{Ꮽ���iL��ie�8 ��5죜K���47r������c�%��j>g�|^<r�h1�����/C�[���ݧ�2�aL�u��L�>�h��ī�zz�Y(M�贠0��>�	�V�e��U�Uh�]{kDf�!�����A��.Ļ}�$��(�-ϞD����ţ��i�����\��$���y�hѷ/	?ߩ֦荙\rS�zQ�^n׃��(����;�I��('S��<�Av� UQ�� )�K*��u����p���pc"y"�N8B��~ˀx�p�l|��ͺ!�r��'���g���f)�Q�H�	qi�p4]d��ì�>�=3�Z��,�qb'����d�֘���*i���O�j�{� �n�+Hy�!��_�LG�p5�lF\�~��얳�H��"��~(�1H��-4������@��Q���AG.���D�|�8���|�5Oxav�
}(��[ca���m0>�<�Prd�|Gt!S��;����������LB�W��e8�vߨ��B��smhK�l�$��*i�Y�[T	$6e����%^'a�h�c���&�U����\͍c�L~6�*'=����>(��J������!`��L�i��ED�฿A���b����F�f%�nT1�|�y�ˑn3]��1��y촾�z��s|�X����^��#p#h�K�q����������;>V�a�PX��o����U�"�����Y`6j���������$��Ά��R�Z3�|�t�+��K���g��m�	t�/�[-�3�6^�@���ܫ���Vg)��q�}�_n_էm)��(=�nÌ��w��į(�aw�u�VF�Ył��y3b?�C0D��`��6����39���1Y3�r�)�g?}ICq�^I�U��S'��剖��VR(UpQ�u}GSŏ&��6v�����]�J��=vLǓ;%�x�1�v����8"a�cG���Kך��j�W�a��=�3���#�@�?ҝ�¹��M?/�,n��s&[��tJ-/�eЫҀT�jy��н���]PUx�M��Ƽ���N�R���B���_=�1�*�*m�y���#5@�>�h��9Q���~1R��qE+U��lD�>u�ټ-�����MgR��m���KѸ�g���O����/ԁE?�%�x��c�r�;�!�'g�ďq\gZ�Q8�Z�q;��N�}}r��������?�£�P3�0cy9w�i�攵`�Tp�j���4m�<��w$zW)7�C ��M:��b!
�C�/��Y}��V�tZxz��^�i� q)0gH��qT��
��/7/n�(-�tZ��c����'�@\�t��1<���CgA���b%�%9�H�Za#г1m��ש�i�
�L�B+����Lf\q�Vf/P5�^���B)Ol��OX��s��p\�-����y�8��j�� aj�/r�+���s[ݓ��]�p��k����^���������U��M c5Bu��dY�a"�p�f%}�|�H2��݌����k6�*xr?�ρ�9b�u���
R��d�f~���K�RL�1�k�o�,`���F#`.���E��v��wT䒱�"�!�$z��{������v�5�!�r>�����#{�4W]��L��_�MX���뚓���v����r�-��������c�����+y��H/��r���h]|�u�<�8�C[7�G�1g%ѕ���)��P��a {��MκK�
Mj�VvsF�6����!���p��&c�f3.5;����R��,��U`oW�x�]K;�	��*�Z��GVq������fHKy���!x6����:��i}����z
_>���'gנ�m��W?�N�`CH);)� CPp��H`��~z4�[ �N��U�	(�Z���[%,��~�V��'&D�!U|+�܍��-0�Ql�Z��E�d'����p�_��kf&R;Z�	j��k���W�V�)D�=�Q���lʎ>�M��I:���hF�ov:?�ldٰ����!��3y����T��x�a}� ��^zk�g�~��_^�Hr1��텗��=zht�5�מ���ע&{Jr�Ir�6\p�B�eD�B���$`�A���� �^d$��uص�l��[ �9҆������_�6���,ܬ��2B�E~6j�7i���E�i�����w5�!}�Ҧ�w�;�)^*�7p�Ǳ��⒱-��x��L�Dѩ��w������D����+p����"���9�I�����y�5ھ*ȭMĿ9��ܯa���P��n�/�m ��[e���:~�Es�Zo�H{��!��}ץ�m(]�¼�i�<�;J���0~	ӥ��¸g�N__��g�-05,o>�N���D|ܴE-������t$@�b6���vᓭhG��/���tq��Y��']zb4���Џf0N�}�6Nl�u/��,W{$��_�3�ye���X"V�8����;�XLNDQ8o��\	TD�r�*l�����_�!Ă8r�V=�x�:tb�gjCs�S��ZS�N��F[]���!��8�}�o#"5��t�=�xH��=鷛���$�$GaYT�_HH��c���3�}��!�����(���b���9S���i7�S{�����"�+c/���	��I,�^'���DZ5����Q�6�X�P���u�L�y�e������>����X�k����PT�Y��Ü�"��W�{&wއ�_��q-�L�l�C2Φ|��`���I�m��S�\��z�!�Ǯ׼�"�6�����֛U1wȃ�� t�I��!Ri)|��֙Tw�B��z"�6�Z+kz;9�+�I�q}�F�I�y#(Ƅ����D?Ͳ	�*8�g}%�iO�����YTPľ��������<�����ɶ&4|ۖ�B`u��+ajG�?��G<�>^�79�U�(v���[�V/�����lZ�<t� F���32v�/H{PC�.?^����T�Z�������y�Q��v�-m?��!\��ĠH厼q��@Ǆ�b8)-����x>��َ�=w�?f�v�	"&"��p塷ć�3Xi�lЦ��kS�٘��!����E� �tR"��t�e��Z'J���f�?�dN�}������=[9N�j��~�lW;��"w�&��L�!��g�.��]��/�y��&��
��^�v���4ↇul�"��W|���)���MӚ�U�y���G�j�1NM��:��N���.c�\�	D����\���[bμ���)�����g���U���0��}�ŰW�!�a��1t�T�x`��4_>�<�_�+}�ey=�oO�^:D 8h�ۤxe���o�o-ȓy�%�=�\*��2הzK�z�4栅=M9	�cKE��aj����e�q������N���z��:�y e�B�hHR4��5��J);���r"#{��2�`�]���S�q������s�q/:�Dm��2{��h>�/���+r������y�����
w�\e��NZ��GS�PG�^iաi��H r;{N�r�Ɓ�v�='"��)��Doġc����C���*�{d��w� �2NG&��oB�"��F$��F�pɫ�_��lf�OJ-�	7��(B+�h��4��
9���mk�pg�V��t�n�����$6T�w�[�YA�H2�*p��V��+�خMZ�R0�=L�
d�����ÚvC���\�����"$A���f�ݷ�G�0X�m	�Y��:hB8]"O�f��H�5c(�x�_�7�?���-w*�D����=t���h�����Y<�
�bR_�(3��DBww�Ey���m�uP��B;���z����TEeϰ��G����h��}�~�Pf�b�lϫ�6���O�br�?e찓L�&Q	w�d.����Pe=^���.P[�2��Bh��l
���F�S�[R�� T���9�yRh��yQ�~�X�V�����D{����Tܜ�j����X��̮:�bh�ɏ*��Vt@��ͷ����,B^,T��(�]�ϔvy��2g�t<��rQ�}���cTjC�Cc���@ڽ�O�̪�yA	���>������f��F%ܾja��^��WJ��^���[�Qt[r�;�ڰ�h2�Fz_wG{i�
�mA.j�)�K��ۭj�����^{�n�2����K�Z�1t�{�T����7�ms�:����lI�:6Fj��oV
L���ўؤ��0
n{����'���(��׉�XpvR�h��R=5~m������&��e�U����j#]�O��}.�3��P>ң׬�Dh�<\R'4XB�\��k�d4������C�~�����2i��L�\���*�3�*ə��2O�� �uHzY���sw>�_�����&�P����sJP9�'��t��JN=���.O��V��֦��Y�5�.%���Gpg�:��}���	����O�~��|����o�'��1K��R�?fC���Gai�V׋���s����P�^��;��X����[�/z��� �����EOQ	�{�{����3�sfN[�m��~ꤧ��R��{��HG0[d��U�l�5���W2�,3����N�j�[��	��5nz �BX=h:�D��/�J�Zo���b�	�?�,I-�u��Z.Էt�Z��g.'��B�)�@>`����@��HJ|>r"���m���H����#�Z�n�0f��(��LS(������
���JUnJ7r�,��BAG����m�P>۰���i�[Iw���Y�Ma���'�.W���Q��N�-�i����q�dZ��N%������`���
g ��eH����Y��D{�K��89�N'��K��
դ�U'p���Ć֭R��zJ�&6�	:��ww�ot|خ�lR�|`4�B3�'"m�n�]��Guϡ#��0��4O�M7�ݠ���]ZJ��S����;��\��3Aeȫ?���v��X��c��pɤ|�`&��ӥ$/�2���i^�1��bo�a�˭%]2nG!u�^
��.�2C��Qܑ>^z�o�F_�9��|���,~��1�ۃ�-,��`���.B�F�[��Uz���ROQ\�|~Ś����v\A��!�+_��+u�� ���=!
:_(R��г�E��e���O���`�����o���θ T3V���/ם.&�4�����1c���d�H�<Dn��8��R�4�v��%����pڃ6+)��xĜ��ˉ�~c��N2;�Z�Y����� ��d���J��.J .���G�6]��i��\
��UUD�������`�
��R�t1�T>���
��a7
kF������-a��x0��F���^�[wo(QU+�TE�]�HRu�.}��.C��cH�U����U�Oi��� E1W{,ܛ�g+��L	V�è�x��tD�V�y*r����S�7 (�#q�XqM_�58��i�U�a�{𠦎F&懓D�KtX�ߛ8	
jB���[VZ����#� O�ٶ������W�����%�����=������~Q��R*��΅M'�ڎ�c.Wl�/^)/�L�	�|o����L#>��]h�i���X�$��s��#2�@檸'����NF���m/�=vh3~���0�\0���\�-��V����ݷ����VV�NJ�u�&)S	�n���Q�(b�*OG�|�1 /#�Sռ�Cmq�M�/��8	��Y�m���H���:�e���@~Gn>aE�#�_�qߠ���B�ՈB����zvD[������.}X��]����K�&)���MAH�5:ͦ	��ϡ`@�X�,WT*��(������w2��M�*�C���3���EM9���:���0>٭�x����-�����X�'!��,E� �W�q������+��[�����d�/'ru��W�R�����Q�+.���'mv���c4�5���q��Kn��=sޱ��/S�o����O���vëq)�&�b8ԼԳoU,�� �D	�_��)!b��)V=[�W!�}=��c�s^��F[��&*"baF8��g@х�@��7��ўS�/���ĝSH����]2xZ��q��\�ͩ��E��98�ٚRǴOo�@\?��5�'!o�M4��c�ݬJ���]��Bz��sU� =��F/m&��W�V�=C��)�)��Y�q|�[8���N�K2h3¥u��q8C��6��"���g�>�*���L��t�U��:# �5L}�'�5aC�
�"Y��^���l0⢎J���t��ȑ,������*��Tlau.YaI���U�K�Z�C�߅S����B]z��[vb��x��Õ�ʏ2���}NO2�Q��J��<=�C~!�}���I���:t[�����J/�If�������߼�JD�=(3-��P��s}����ԟ�>�'�|VQ�J�3����o�SC�D���6\�b�gHxǠ�
V�:з->���Z���J *��n�O�慔��Z�F���@�;|ڡ�Ll����HQA�����᳃�q��_�鿀��G+0r���^|��QbIܟ�7	��:j̝/��S#�/���T�Ы_�Γa��GU�jP���`F�I�!6s��\��� �O�5�jF;:v_�8�M@'p]�*Q��oU���r��n[�x���;(F���Aa (�s�w$3��=��^��Ew��A���t�g�M����~���a�/|��F9�7���M3���M��v�jc~��Nn;s]������D,7At�:���&�YRb���V�}��Q�ȉ�#�XȎ�7��<2�ZH�L�{�<�F?��7����tg,����s�\���Ԑ�̍-{����U����߈3b���0��k��PL�(�yd�u����Q{}����Ꮛ<�#w�m_��im!r�EGwq���^���lKZc�ǻf�}8�@��۬�E;�\U��2�P$nV&34�B���1ل|�Ɇ���r����j���r���(.��4��1&Dk���c�o	ߩ��~�p7ywRI4k�����M#.��x��E:f�=īҥW�6�!J���X �� �d���4��R��'OyA#g�p��=ћ
q2��85�g�q�a���mv�Ϯb��J8e\��:9�/=S��7��+�6�F�"U���l���X!�"ģ�8j_�r�9y�8˥t�0G��Zh��(��(Ş>fƪo�I�hcڙL6kz� +�����&�Nw��������Z�`�0<���Q��e{r�0.+|�ꞨΆ��%=���`74_B!�;��ا�'-}��l���2cý���n��-{����Pf���	,�J�y�ɑ����=�K�^�U�4_^4�Z1Z�%�:Fd��$wӸ�X�7!i�������^��*p�P�/��t�����\I@kqU[ٌ���w��ܼ�K=��?���'�n����e�!2���}�Z���o��םmt@o�^�c����v�׎H��y�+ͦM� 8��x�w2�^�� we���v�Y�9����|p�^A"e0�� h} Zܝ�a�fM�CuF���&2�H?�k�.���9>D�lo���AǠ`}!?��zǬ��)�s�ʝ���t�O�@�L�`�:�z,.!�8�U��q��@�8�����@�Q�{��@UwK���)��	"&�̺vz�x�1���Y��H��U�R���=���]�%���#=$����TdWx����c�����g���V�k,�	��js���Ge���,������\� ��~[{�,B��0�>ڽosǿ��Q3��"��w9�v�Z�2+��K�&/^��(�M��/��)�q�����
/��$�MsseP56>�&d�1�\{��Ǆԋɜ�D��/eOu����b�NfO]�q>j�������¢��iX�����.c	Nõ�{���:�] ��@s�tC��v��YE<��rb�\oY��O�l����Ӿ�mH[�Fn�.�,9]s.ln\+J�t��o����St��$����?v��\��Zބ�2.
8��0��;K��49X��qsK" �U-u>#$���u��l�q3#�,E��N�����x�������{<��ɛ������f�6|`��tL��10	6���Q���g�Y1g��}O������Qp�-I�$vQ��!3���ʹ�d����jގ`�W�)pC��[�I|,	����0~#*�J'��2��y�d֬�Y�c��O�681tw��Ϲ��דh�.:?=��0)�˄�w�ӏ�0��\խ�(�#���VS�v�`�N��
B�e���e��3@���l��XO�Q��P�9�?%����x�L*�w-,6��������|��۝�z (�Hw�P��է�~�NI�����{�U���v�}s�����S���a�"�I4ے��C��dT��l5d���&&��xcr)�b��ў4���А�v��9�,0��t|���r�'�Y<�}K�&Vtf���l��l��_��V��é X�����lkq-b`V+d�ʀ��#��TnwaJ��?޷.aWѿ���jej�e,����Vwނ�Ζ���������Lz�Z��>�����h��W������L��.��N�K�h�!�y�;�+S/T�rZ�n"yZ����U,��d(��9��"�	��&P��8d(`<��t�	���?Ȉ�}i�X��b�=��ߓ��������C�cl��5Zĕ��("�py�í�>�$8�֏�LJ�KMvb�ta�.��z���E����%���i!�� yh��aRŦ�g��.c��u�o�C���P���w;�d��x�� ��u+�۹��m���7J�\;MZxo|"��o};e3"o�|��u��W�G~Y9m��ژ�U]8��fϔ�-�i�C4V�o9Ԍ���V���g�hu�������?Ӕ�r0���|��PP��i}*�_[޺��4�C�� ��qU��i�b�ׄ}z�=��L�ܔN��=�`����w���!Fb�ďE@�U̧�E��5�}��kj�wg@�&jA�m�p��a�.Cq�m tL[�.QT�/h�H��e�ޖwo�H�'H�nw��6��X��v���"H��X�ϻ����q�h�m{Ֆ����Z�}B� P<Jݧ��Fg��B(��X�&4��\9�8���Ҥ�����a�L)��,�3T��>�a���Q��}�'�Gra��j��4l�n�>�����h�Db�r�@�%�^�*� ް�5S8�����Vb�.��G�b4��+B���=}Y�N��:L2~�`��!���x�	�x��G�9��+�[� �=�9�H�0 Z�!�Ć���p��;HV�U`B
�`�����䴥d+gl�����b�ɺ%Q�Z���Y[򊦂5�/���A}�AL��w����X1���7ܫ(��ŇY��9�	
z�q��/��7�G��[n���0��Wm	��#{��E�'�^��=��w�7x�����[�����n��^�M%��>���;�Vl'����24%O%�$�[�����'zZ�=����_��|Ro���-�)(��*�	�h?s��0·8�iwp�ڦ��&���_�&f�]?ǜ�r�c�rV��Ҽh���E[����o��VٰB*'~Y�#(���^�Qd.J#�'_��'U�Oh���ʈ�o_�<��@���dDi̹����;t^�*�}���~�݌�A��KU���)USH��J{��@��,NLp؂��CΉ�sHM��r`nE��~����� �Z�28��뛴h؛���Y����R�:{���;���aM��q!h
[�0b�x]�F�;�Ė�Dj��u$�649V��Iuu�C\cM�ه������#�� ';VP�#�_f�ɊR��[���ԁ[i0� ���YFS� zDwOv��9�:��s!�3�s%$f&u�ɡ��_��F�tk��j.����2����E�}>��L򁻯N+�0�w�� *�3J�z�de�w:Hi�%���C|sƮ��iׁu��93?�;��*Uv��mmu�b�D1Ym4��`��<c 1�.�T�}�)a7��u�e,y���g�d�9Wː.	���?	ص��fӎ߹�1�lc%��-�I��|��QG��O�gʲ>��t�:! �nQ����0���,EW���e��\��<7�z�8�j�)"�fWǡ9�n���K�c�ʎ�*ߕ	���=�E�j�t��M&��]�^~�^����`^������@0�GN�)�1�ss�
�	'��E	�11����k#v��Y��X��9G_m\Y���T��4��ໜ�X�)�Q���v�c���WIN��O?��|�ޥ�T�b���|Xh�S����4S*���9^ލ��������%��8:i����!d�́�j/K�o&�o5!r��QHJǍ5}dh�+eo�ȑ�9��v~�8�a-`-C�hG��V?�b�)�v-P]��-�{��Br��k&��#��0vl���;Nf���o i��9ʙ����"��8N@���������BY;�|ێ���P���s[,��b��b�^���2�����ѐ����z7�&����M���!�Rh�t	�t����i˘���`
�.��9�T�Z��1TN���1����ehRP��
�Lϴn��˟w��K,{�<&O�#m���D����M�c���
��U�Nc���ƿb9��}x��kpI�#ۧlp8Ui@*N1�}��m�B�� �㌚�Ȑ��i7��)�n&���V@��������l�=6#�Է���e��"��;������3�\`���X3G�&��{��!�!��Cp4^��br§�0���7�#����;Hz�}+I�HH!>;7dP��M�i:��G�$��l��G��%���hzSR��Qs��g-�TXxX̔����>	���}���H���Է�7�k�L�2��{:ƫq�Vf $r:��n,�>�Y;#ꉛ��Ve�O��6rJ�!G>޶\�BT��Yd�T�N�|�v��8���7d�{��!��~�3����G�׎k�{�XL[R	�T!l�H��M'��H�םpX F?CqY���Bc��ne��`{!HMNN�����2b����@ok.Rܑi�＀#���q���A����1ik�����|��#aJ=~tHn�|�\�cE���:ld',:#�`�lѪ�z����W-�־0���TO�s*����YQR��U)?��:��K�z;X���_������\�2}1Jp+[��Բ�4N���M>% F�����X�lɀQ�n
�_i+�)"�;օ�D��J��d��Ϫ(�Ü՞�������!m��L2��$���rߵ�r����"��P5�p5~�U4ƶXH�h\�˗�۸�E��Mg7P#C�<�
��H��r�*u����c�M�~GwXX�'�|��B�ȵ�-EJ;t��sDlOȣ�vھ�42����@^��Z��1��t�$�Y���Ӏ��^mt�O�=���<r�����2�L�p�Z��$��!V�O%�1u#<f���`Hg
n��y22�љ�ͦ�//c�zآ�B�H�9G��4�.�U��nta'�����'.x��z}���PQ$@�@��;[�󏝆���*�4]򖹓��y<�|_�}��=�B��ZD������"�e͜.s9�H�m�����=��,�� ��hqc��ͨ�ڢ�
�vя4�ѵT4Ar�
��g[��~Aeeݐ��y���A�L��~���%� ��6��:�{�/fH�rH�0��/	�P���t�̆�x�P�p�;�����)5a�PE���cjّ$��O��[�J7x&h�}N/�1���dV�Y��b��42����s�>�pO6]%)T@�-�E�SJeQwN���iץVu�֟l��?�v~���B]�P5��ۑ�L�q`:��tW_懆������d95�A�����!T���N_�����l�p�D��j���/%����޿�����f�}7:��x�3��-�<��$KK}�q<�J���==0��v>�f<�Ɨ�~���¹��xb��fl��hm�nX"��B����3�����{���[�s\z�D?/�<3�r���M�Q6��F�p�<��c��Lu5[��p���ku��,R�ǠN�ċ#��G�������=Y�ືe��������v�~������ !��#3���VHf�)LZ�\�jh���5�%�b�K�7�`�8��j������c.G��8���H)�����!�	m����?b�-��"I����z�>5�#���f�g��?���}��頄β=��Dߨ�y
f��V��h�3�lf�E8ᗭ��Dw����%A�y�+��%V�"����v�%����d���K�9>a�`!f�f�hh�r����x�c���2��W�R��k����p79RDMn�4�4�L�d�����5��i˷��a}�t�W�?�8��5+4��˔���)_���)���L�ɒ�J�
/�چ�Ⲑ����^�sqh$<��*'Nte�͟�aҿW�ʏ���x���y�E��\_�U�[�|J����&�6\t\'�f�r�M��)�`�$���:��YF<�E�&S���?�UT]K���`��%ٸ��F6����`��%ww�ww'\�w�INN��{�o���������U�Vտ��M_��V�j_�Ҳݍ*���e�X�¶��I��U�o���I/��`�[4D��\����ow����e�g��cX�ic�NA&cZ�f��r��R���c=�SC�&vݼҡ�8�:����(3�Ҭ8HM��טʙ��ߦ�6�cs%y4�����4Â~S�Cɇ��^�#hT���,נχ�^X1��B�s�12�RM���r��"�k�S������'�	�?�������yS X^�6̍��JJ*>���f��8(Q�"긏�k��L�����qO\vT�;�]�@n�<i��7�2)�MNT�J�袶���ͽ�����t��3�?������X߻
�p��~i(K�R�4�QY�B�XL���c�3�G�E//����ޕl��[jE" ��x�G�ܩ�Lq�Z�q-���R�W�au���9����/����GQ
#���)�KAdV�dB<,�������%7���󏚂�V�msL�* >>�*_�=���pŠ��Y�+WR4E<Cy�p����53�-ǘmDU��ѡk<χ6wK��u���5�>��:@�2��3�o�"���M���%�Q����bc1l�ȧ�x �n��/}��4Tm@��顦WZ��6���Q�?�2���R��3[.4�q�$ryY��|�����-���_'�T㋄x.*���K�j6�����>,J�B���[x'r���i�}a\���O��FI��L�՗��[�+�9�<�&���c��/�N��oW?
����j� !qP��{�3M'��䶾�����*��K�.��>����
:�@(�ܙ`��L��Ǜ奂~��A��e��{}��~�T�4@LlPyYa�a޲��4'��`/G�雊K(_��s{-^�P��,�Z�E���>��>�F�'�h F��m����S�qYs]��;N�ȋ�c��4U�Y�𓞹˦,�Q��{Xa@�5��j���G�/a����L,�#��(��ԯ����˨��(�VH�Y���Pdf�L�vk��)�e�2G��\���^imt���Z�!�6�(:V\�Ğ��,$����e#6�:��\:X1h�k�@�W�	`N6 �A�J������Ǒ募�FՊ��ҩ7�r�e������ޣ3�jl�����WRe�2`,r䌌<d����r��ow_C]H3�F9(��F-*���D{�M_��/7ܛ�e���#,u��K�����Z5�$b�@="�sZ�<D�X�wL� �\TDb��ވW���!n��#���r�� ��S����K�X�sM!�����a�t���0+{9�l,  
`��1AA���G�������j!KZ�T���>B�c�����H��ţd��|[�qW���U�q7��>����S�x��?����m������"��:Ģ�e0}.)IE2��[�K��a�Y.�'H	|t�R��D����;�'��V�\t�^�u=�v
D��\��h(�q��44�=od�`/��E�{�%�INtG��h����@O*f�k��Vh*�أ�S�c�8�B�['��8g�`��$O�-`Ia9p`<-m2��z?���uG��U
�՞�87ةw�`�nL.�#m�thhJ��W��ߌܶ։!Z$����;�����_�J�!�P�;�C����U�L����ؒ��1�����T%��%�;�)�(��#ZO��L��ߐ~{�z��u0��Xߨ��p�D7�`�wHp��\�\��:[�IS[2���Qb�{u<e���OI��J���J�P��e���F��xO�h_�T#һn������x�+���եŅ�ͫ��k{#aJ�i����bc2��p�{�k��shM�C_���)�+0w��ۂk�9�L�ѵm����P��sX�Adu�q�@`�S?�Ygq �I�>���hnظ���!W<3S���T�&軞74���Z�X���B���|zWl"R��֥+j�w|�}����ʉ��/���((+y�j�-S<p��X�+\p%�	�A�%�u���
�o��ɷ;�w5����$G3��+���*�:qH����)C�'�{�EK�Q�m9��`S~��BZ&;�-�U��݆G �{�>�-����V�"ȿ;�m{g�IoX1�	�<��c�q��5��!�#��U̯�®x5����}22���Ȍ�5�#�䂲�ڗ�̣������c����F�]�9$?Z�Ĩ��^�<����<Y�!+(����;��Y^�<�Ϳ@�H����
Fz��J²n�����N����F�X��vaـ|.oj]����=F<	���K�9�dqY7�	��r�më/f��Ewy��-7-	�<O�Fz�x
��k�����(zZ��Բb���;�Ѓ�?���G��\�2q����aD<�+�w����}�C�����G�+f*��#���@E���Y�����P���L�&H�"{���pVn�|����p2���8����u=c�Z���[r��(R���]ɠ.��^�W�rE�>��|΄��ve3�ps�����%"?��%�;]Y2�۵��x,Ϲ>�����"&�:j2�d#�E�z���]����'�w7|�O������'q~�j84���:�)EU$�ༀ������;���[�w�Z��#B�{젓��*�=˘+��*0�(�U�U�{d�}�I8�!�+�Q����0�R�1�ĤL���h��V�@,΀K����#�O�V:��c����-Q�wl�[B�?����޵��+��+�y��d�^@�{���[�t->.v��7�u��1 ��a^m�gҲM[�ՠ-"�������mվ���}��APOO��x����3��]�,6K �����l���/������.��t|?)��IC]�g3D'~FI
��=���&�yP��bi�=h?D�A���޾n�#a�0=� ނ�Oǋ��24k�O�*%/q�A�;�d;�TvG����#t=��ih3��!���l���D�LL��Y�b� ���m鑛�z6��Ή�v����{�!���#~�\S��9U��)�g�]��Q��٨{O��+ӵ_�da	�Z�5�,�$,P����jI���L��v�2]M�&G���|I�(ủTkO������ҩ������� K�5�Pl��;�`�|�0As�FX��_��a�|4�ӆ)òQ����l���������<�D�H�#q��{#�!+1l}��0�@�j;y���s����]��U�`���S��S�����1�ϺX(�[ݯ�ִq/-��/�����[{և����sg,UA�<��z̈́FQ/�	m��k��=&��-M�2�%k����<��.�xE����Qg��bG~M�2�]綣m�?�+�a5]U���34~B?�������m^��y>������V����e�%8���PJ
����UO��7׍(�4��L�?6i��>�|�孓.�|3�z8b�������-~��O]Wr��+�RN.Ă��I�lCa#K�=7��`0���]鈅��˰��k���6k�iP��q���@��'�{w��7��5q�q�>���I���ZۍЭ�}�Hj��.��]`�
E�[�2~R��g�#ٴ�3�p�&痨+3 cF�Y��Y�:�����(̥D�;:�a�qU�*P�u�>�k,'?��mC˭���H-S������-F�#�����4�%����>�HFt�n�M���.��b�j�����v����)Tܯu����r�ULL��8��8H5�y�<N�����5����Ly�M涆L>��g��\j^3^%4�s���{e��8g]��)�!��;^��zXQâZD����f�zD�ܐ�tzo8d�z�0�������&��L�+i�io���#֐?���~=��k��'z��]X����=@�s�b�iq��e������$r��̦��3�G�/C����v�ߤ���f�g$�y"���D�q3�S�KDfk񈃶����}��V�n�7
��@ُ$ZR|Z��@�ڞ���jֺB�j�U�$ɼ�.���S��凴����⫽�{o$�/*Gi�HjYc�P~����,{�ojE������hA����y��Sc�*�'��������$؟�}>κͥ��_]�u��g��g?�p�]��+ҝR�8:N]c��ٟ�!ac\/���t��eY �+��Hbd�v�彫DW���,r�A�X�HM�ɨ��~�����{��N�X��1?��3t� mF˿���NN�䯰3�F[�;|%���N�@��l�����{�`3��� R�iL��0}��06� (lֿ��n$�i`�'|���n�����k"��E�bު5h\H���U<��DO�(k�;!s=�&UNǾ4�:�C���R�\�:��k��l[������O\�l��|b��?�V�
%���Ӱ�tto@(��K6.~�loQ�a�$ĔAhP !�^���0�)�Z�$�a���P?�I4+E�S�S�gD�wc��}�Oә��/�הɑ~d|3��`���ͻ�cx�}H�z�
E��yE��O,��F4�3 ���5r;�^�����,�����]̡��2R�����m�	�?/|�_���%����\Fg��nG�H��\ќYĸ�q�L��b�	r}jL���g:�ʼ�~Ӆ�n� /��AU��!?:���i��	���G]O�QI�\�6u3�x�/�J�&u�M::©V��ǯrv�}x�j�on�bHZt�;�qc,��p� Ej�+��Q�Ou���OE0�)���X���i9��*6�"����6�I�*W��\���䄥�!|M�'��9H��VY�꿽�_�A�؟m�U�l��0W��������t�i;�B�4o~a���������N��7YF�|�ޫ��#��$����z:��x��G7܋gE�{��T�a�<���ƀ�(�&#�����q���F���u^�=;�Ϭ���x�-=Q�L�4e�"���׸���[��4Q�8��!v�pyO����g�̪z��2M\�U>��Q�L����Ӈ_�@A��G��1ø�:��8�)��!�1NXJ�h	�]��3�H��y#���\�=�^t=#�g��ͪq��\�id�U%�ђ�ɒ�Lw=�2}���`����|oww��T&�5��N�+X���{ҭP?i��:/tR3`q穳}�Î��8OL����dn������0�zEI�*Ɵ�Acc�)����"4�\�p5˧�9�z��\������o�#A���~UT�6&��UY���y-�B)K����|l����S��j�J��!�H�����VC�nJF�ί�y�;x��W2\ߌ�>�k�ѱ���;�wt(�BKø�^��(��O�ͧ�Y���v��؋f��<��<�p`�h'	�K�z2��N;+�%.�sS8��`�_����SU���Z�/��3uB���u^�CyP~�	I�� ���. �Y��4\��0��dr-��.\:7Ņ�o�&l�	E�QX�e�<�{i�tTY��X>��YҷdM8���m������h�|a���_")��_�q�3*���hcL���T��c��HX.�����m�y�c	+nb�,�f�KUtw$�	�*�-�J��^�[w~�[��nNTVW�s��o5��Uet���d�QF-�~��p�{�IR]|���$�檡)���=��(s��R	�8�ͽ96�?".y�d�qH��x����B�n���kl*Ӑ���؀�݁A�io� ,�V������*s{o�ߑHK3̖z)ʹ�0z��w�C��)j��$�`\�$�wK@�G����v�uЌO��^M�\����V�Ac��c5����)� �|�l&�D�pz�.��W�/!�Z�����9��q��L4����"X�n)�ġ��*f)_h�RU#�Y�{�(�l�1]?��/�>q��
���T�)��Q���ވ�?�hO,�'L<�����jK"�D̰���.D���&/T?�;w��)i�Z����5e'J~I����<�w��0O-�8��Q��ux���P�Z�
�p/�F��^�wJ��g�#����Z?��B�ɓqA{�Ċ�����C�_��f�$n��]r{މ&��{�Z����.e�߂��?TN���#J�P��b�&ˡ�YΒƦ���>2[��OW������8�G�{g��������B��B�pst��x�lI����ڳ�4�	
��0�G�G� �v7c%��k�JNxc�� �����6��.��ϊĮ,+R�_~��*�^k�tR�;]n��5!xak0����u��"��pg���!���BN܇�w"�,��:3��2p���]h�(����u++�o*�����e���OJz��#�_��3 �	\b���_�+ZAy�����z#e�Ļ��?��W03Zii3�!I'���
�]E����=h)�q�ۭȿ������OL���E��1����F�ˤ�;���vջ��RpV��q��CWd@��aБ�s�q?����q�tu��½�R;_�s�Rk����@�Er���Ė5]4���۫��&��0yt+@5�̦�������K���+����[f�k�Q�q�漾��	�����}�D���aJ�T�N,�@]�|O`D�
�+:�e}�q������5Lf�g>�aܑ�r��:��r? q�"z�X�ӛ���&E0�F�
���l�Ʀ��O�t��
���V�$G�G���;�{�˨:���Pl5�u���$i���0�v�.����<�9�U �!{q��
'ε����9Ds�_p���h��%C�ݣ
��3Cu��Y��x��у-W��&�m(���{�_h.c}'�/6�s�j���')��(�uЎ�Ey3�ȇb\�8��}��}�F����l~�s	#�Da="
�gܒ�ل��꾢c]m��d��J�a�D�k�WZf��L.aA��D}a����$W�_����$/'�{)�5�%�^9X��E�QL���X0_�1sZ{�P�����+l|Mb�+сۖC��)�J���*�z��FX&қ#O�.�g%���bd�#(���W����6�_���2G���.R8.]7�]/�����c���ߜ�c�d�ӆ�V����S�ߡh�v����r�&mgT����sH^�z�Z_��[���<�x�b��6L�����SG8����ً�`Շ"F�?�^�Fy�,���}��jxq_�sv�𔧉6»5y\K�ak�I����ʏ�
��ۉt�T�ޠJj�H��@Wn*ٵ��9�L�4��k�u�X��Y���#�A�!��_ziX�Җ_vi�(�(G˦�$��w���Q��L�@�h�&�z���!ĝJ���L���^Ju�a���Ԏ2h��-dT�P���t�D��Xq��T�����u�!������z�_���?�䖙YqHO׿7M�H���p�������hN{����S�XԔ�*��;X�+0�0�O�f�R?V.!qʛ*��y�G�-��D"��~�R�og%��-F)��������1���c���_$��$�E��;�TU|��*F�6J'�^vۭ�l��.Г�=��{Up���_t�!���7P�ʘ�A�G>[�߸?;��o��R4a
�@�e�m�=�4����͵υ݅����m��w���K�HV��\!��rϴ�LDFEn�����;x��s��1�9��͋=Ԧ8y6y���ˑ�CYZPP��W(�!	s���d��R)6&=*$��"*.;���7:Ho���'K��r�|���<����ܵ_��������,��B����♬JHwz|f�bƾ��C���7��KJ��������o�I�s.X���$i!��ί �8����B���B��/��x\�?�[<Y*�?�}x8��K'�jQ�fx<կ�a�}op��dW�{���I�^Y_�E�-�e�laD���H���i�|l��O�jm$��SS� �ۂ@mHv&(QU�cL䇷Z�_����ȁ<nJ��^EU��Gh���	��Z	��\9�s/O��b�f 9�h$�<m�φnNU��4�%���-}p����R�K1H���sO*��������«W~u�E��@�	!��a�Q���N��m|��D���F%<=��(�?��9b0����A�/r�����N+�I�^��.b�L��^�x	��x@�)���>�U�~���+J�B��x h�zTŠ�ҴfI��b(�&��㉝/�Y�_"��6��=O��&>�R�[%��r���{xm��,���\��uUʨ!̝B�rݕ��^�ͺ*�ZM��<�����<��.S��[�j�e�	�ޣ<���5�m�-�i�ñ�r��qj�F�-vP�UD@��,n�_�V��Zw~o���S
Qqŋ���4=H2s��
��$�D��ʞ�9��=�{Q�O��L�z��]��ǜ���c�&����6���Q�����.�77�!%n���vW����w呠⿧��'�W��?H^f���T �g}ݻ6,������@҇OK�3P�u� 1J��!��B�_=�1Ы��x�e��~���;2��h��N{��E�y��CEhV%�E�V?Aq�v"�̂�4C\|�Ľ��lJѧ+�{�F�����z�E?c=�jO��x����U�����t.�Y
ϱq�-58�+9wJ=���w��W�S�~����@!*�`'/�y0�>zv^+gsL�L�e��%���R�J�͚V��y�u��I����
��V�%Lu�ߺ�5$�zb-����I���ʿR��)�����r��Qv��"�^#��[��E�����]Y�m"�6�6�}�d�o48'2EMm��%�뭬S�b���K��cf�R�6|":.�{&��qs�F�W<�R4����T��JK�*�^�� *?�b��r碻�������bsb���b(�5��uF#��WW4M�����ѵ:�=,�KW�"�4���4���י\�3sPO}�|�K۪U����`�Y�w�0����S��{S�"���dE����9sV�Ke`S���@G�f�x>m	������҃�d��ٰ��jNn���d��(��:2����Z�]|�-!�_���a�9~��{Ʀ�W�[�,�g�l	F�7O�O�'O��h�k�.�K�Ǣ2_%�3\�n �L~%r�����J,���Kf�6J]�n]`|�:~rcH�1���w��jI��.��o2u9b1P�	���sb�u� K-+{�Noק��'��`r�Xl�|"	�jF�>�M�!	�+��qE�O*��@E���o�����X�s�vD�Z4R|��d�2��ُ7y���i���Rt��;^&n�n	���[:>[�.���_=BWǜ2WW5��$��K�w=e����$�{k8��g����H�� �&x��n��eh],��b�����՗�;���U"n8f���L�w}p�
�1��E�5�i<�l���+��/y�X�P�����֕_p�>#��=N2<��3��b�]6�&V�mW�4����J[����T���m���^VB�;���u�Y�
�0i.��<��f��&�<���t�0s�{K�NO�wW[������2�=��K���^�sQ X:^ � P�;�o���JZΔm@�#R H�4�l��ؽ�2� �T�נk����髢7��a8U~�4G�0�m���N�`��Zp�uW��n�J�C�n�=���g�|�h�p�G��G��a���x.���-��΂�aY��78�z���d�c=!��E�9�%��b 01��F��~�K>�O��Mw�K�.��-k���#�,B�=����,��`
��lf�`,�kkʗ���*�k�+�I5.Z���"q����n&���Z�T�4�+�l�%`��[*�s,�*Q�����')h���=��c� 7ӳ��U���Ga5���&�ؓ�,�2��P��YqYvt�vG���}T�>��}��$0�C�|�9ݘ��@�l�� ���7H��Evc��w>��ظk��Q�3����Q (*�{� Xs��kň��NN)ʣ,A.�@S��w~N�U�M���u����_������~Ft��Tw$�l*��_}�Վ��"�'[.��Lݹ��9��?&�@��T d}���`tf��w�*�F��������g��@����Z�!��B����� ��Y<$��D��F�ejd:�o�}���HzD/�$��L��o�� ��?������5�wM�|*��j�Ơ�y+�|�����&��I��E9����^����<�B��� PK�����  �  PK  o��U               word/media/image4.png�S\M�6a�A����N�������%X�������]�����{���Su~���ڵ��k�^��Z�C��I����y������7o����!!�}Ս޽y���E\D	�~��N���l�+�ɞ���59��~Q4���aY�������o����͎�u��k+����6qߪ����H��ے,�48���6����;~��C��� �!��[l��O��A!r���	_�`�O�p���K�!t$�y���������"��ߪ����X^��O���g���-R��:�,��Q?h
�	�������[]9�3C6���E\3�ꪯÎ��
����Z|_쑪<�*饺�\�@���|}[=w���;Uձ1Ƈ��C��WQ��Y�/s,��=����@~�"�u�9�O�.~"��/�� r�b��R�yz�qrE��翍� <Di!e�٤�١R�]JI�W�x��E?8�(=�m)��6����`�{K]Ge�}\��Ǭ/�X��vL>��'|	�`�߅�V����ډ��Ÿs196P�ok�����eU'�N7�@�B�'�l��I2��G���6����W̋��T掭�Ի��_��s&������<S�rI�1�Y�o��W��1�:��]��hN>�~�Ŗ#�h�"�}p��PLT���y�Z �Q�-ډS����Q��z�\MoН����	x�y��h▐u�L�M?`%_�/��3Z���������>�x63�AA���;B�M���+����A�����x�؀&�Ƣ��֥�j�^��u�k���sdrQKwF11�/��ؗ���l����ZK����ŋ\d�ӷWHu�x�5���*N�]-��v�ѧ������!0e��M���tG��2nJ�	��	Z	��']}K�?�s(eEg*RJ�%��{3w�À��t���'������x�Y}����ǙY�G�g�S��W�*���/z�6Κ�zwI�������rT��[�>$LV'�[ Áh"D�}��q?|R\:�6��p5����:M8#K\�U!�̅=�c{b�T��1���u��>�G�!#]�]���3�l]Z�5R���l�#=T����x�U~�B�x-���8��9[h�8�ب�oWu@1%��@_轪�����e�x���e.n
2��hl�!3��c�F�;h����y(�������7�J�g`�G���H�|�zO�8�F�s����/�t|�(�b��2��"כ�Rn��j���P�G0�������}U^��Sd�np��	ħg�*��@F�n�����|�<��a�aS��K�]����zH��{Y����E�@쇅�]�MGjkS��� �uY^eL���'P����XM�K�X:d>[�D�;J�O��^�h�/�F�����>�jC��v�d�=V��~t0cη�Vy~���xA��uO��e��Π�����c0����VmW�
-QٹgӦ�(n��DȨ���S�!�C���	�D����B/��>%@$����1ѓ�'8	ʷ����J���W����n�s����C��� %Axz����B���Zy��<<��HJ�z��ǉF�Qcc��W�ZrNد;YOġ_�5T�[�69��B���׀��O�=}��	a�Ac� ja ��Uu��"�X=K��k�A���@�AҸ����]�6���a��u�{A2C[�s~0{*h>Yq���J���"	(</�طʢ)��=��ߝ�~��0v�8�$�]��8|c����7�	�cAÃ&���i5|_=�Q�̊�{^��f��id]�G^&q�����/d}����n�G	��=D���9������x�`;�=�����v�/K���6�4�(a4�Ң���r��|o�+N�7���"*�����T���MLn��P�ѫ��o9���=~IH��rƅ�.T�jlI~�\X�l��]��O�}`�����	j�'khզ�X�-�+2ܔX��]�9[�*m�p��9�Y:�r��b�m�������a@�0q���r��jj�@�_��%U;g8���(�y?��x�4�\ �)�4��A%�J��*���@�C�`T2^�N2~�ǌ5B5<�<�	4u�� ��p㙞�WA��rנ�靴�ⶼ��!X*Wō��*+�Q��det_9�㹆i"�����A1-�?�k&��T�V�3�~ָD�ds�;� �?	����|�YDV����)�L��~�Xk5PFak�q��sw�Pg�͞�"�7�BZs�p�U �� �!�O��W���8�r^��X$#ȑ��!��%-0��1�0FF"9�r(&��Q&����z�2��9����k?�x4�o�l�ʸ��-R����"b\�+f��+���C���6�cS?��y0MK)4;!?ƞX�5���P�i�1�l�	u��q�N}0s+�H������"�Q��bk]�!�Dt�k�}�E��@dY1��1��"A�	�:�>�~��C�>�#hY���iTF���SEI�
z�Z�:-4�j�;J�������JF��ʑ·Y�Ҕ*�|p��D�+��t7ڌ�G�h��*v�hd�l��ZA&F���k��Wy�4bX���A�q�q��=����`Po5��4��a'�?��P�H��� �����c���w�A���u�&9��0�/0�"���|[p�Ƚ΁���̞e��צ���k��Paez�w!��@:	U1�AcXɤV����4'�g��(�]",Q�;�J���,m5"�T�[�%�,�+�͟M|�o������?��5fy���aDٌ,�Ј���^㸘���1�����8��¯N�dBn<�|�@����E��qs�H�{8��I>c��Ng���~��Y�ˌs�w���-�r�Iݵ���%��9�\�K�ʤ�l8jڪ���z;�;Jfm�H�E�<:�WK��e����sw^~�I|p+IP]:`���Y7���1g���!���$����$,�ڈq���������]�U~81��8ee�zl{u��~�'��1�����%g�ܟ����0	��~�_tcNT��b���M�^ʦ�ƘR|t�#�P[@b��w�z����������h�s}�*`�c��_��7��t5�I�F
GA��]���矇L౴Kzw��+N������#Ny�F��ΫD�r�g�H)�A�I2;�\.�С�X�[�WY�l\�Z�?0�А�>y�̺�	'�,Rg '�r���&v8A�#���9	�#C ѻ� I�����~_���� ��	�oV�r���q�	�~mtb���N|,�k%ٓ��>?�|���jč��=��a�
_~V��?���~8��po;BC�q"(��@n�j��g��� ������bA"
g㪁��5�A�Ӎ!�-�]L�jca^���L�$�|3L��
L<3��\q78A�3n�+��-��Q}y˷�Q�\&�̂����a�!Ioܰ�� Q�s���4�y�>B�C�GCB%ScY�W��O��k������X����+N��I�$FP�%G��e�����ǌ���w�GjuS�hf�39�3�y6��&�[|V�I�-�[�O��MD�M&f�u̖��*yQ$���\��O��7���a�l���BfU���R�[�V�K(ctp��\�l���%��Ҫ�BZ��u���8s=�u��c�T)\+cL�yx?9��ȟ^n@�������������[( ���B�Xx2B�?��"�.n͇�m�X�gi���4[�&�V�~�1��ݥ'ry��ZWd�ۃ_��	��o2*�A��)��1v�ȳ�&���i6���#mC\�<B#?�Ŷ�[nی!���v��� �-<�bW���9P`�����`�6ei���6��ã�I��f�
$Q�-�K�E�hA�'򁏶��B�l� * '2u)y��|��R4��3^�<�R��A&*YJ�vc���?֫oo����WJ��[p��1���62�?_˪d87>��P�}z]|��CW�/'b��s���ss0C9*�_է�]ƯN��ʎ���ؘ��Ei9�����C뉭s$R�1�l�(�?~��)T�P_ �B�^��xG�D�`�>�-O6o;�a?�LS���:��0�5��ç�;��n�6/�R5ȅ>���lbˉ�����L�߄ ��:����T�#%�����v��M��}Q"}[�d$a@U:��a�m�-�v��[����s<-0��q�;v?��H�f���7P#����*ʩ�W�����F��I��?z�8�\���M�s���n�2Z��z�����}99m$�o��T��Y��͒�c�J���� �����Y�+U�;+3�Q��U4W�{�p������6�՜�
J�)�v\?�|�_t�ZZ�t�������3G���>���E�^��32�l�+F��GQ.֫�=	��V�i��F�-�|�v>~eƕ��9q�<h��I��B�\a��Lq'I�8Y	�<���܅�U�Z���0���7������y��6�
�q�ދ+��H$)#��Z{,��!�'��z�80�,J|B%��H��Q��e���_�������)>B9FkeUֆN]�U�@Ȅ.�����H��i(���j�����^u�x)Q�X(�,Y0��}q�IDN���"��m�s���#�R��`:B|�G��'����Х��G�_��a:hE��Ƣ�/�V(�O�Q�q�X�rqd{!m)��_��<&	g�Qd�����!�I��Q$����\���d�}��8P_KA�ٷ�n��¨T�15�}��^��ݮy�B��-�ҷiz��}��ÎV�$2 c�h}p`OU��{H����L�1R�����<�� Bc$��WQ%Б&�u�e�?�e�,EQ�Tt�]k��s?�3�sܾ��B����\Sc$/҈Ns�WI� �$ra����A��%1`'>���a��nA�'e�����J�kC�P�G��:���6z-?R�2�W�]`
���/�ؖVPڗ�[UXD���ѥ�D������H�fC)�$ἡ�r����؃L">���+�<�'�Jd�6���2�$�r:5��U�e&.��� �G{�6Ʌ6����|����|��۝D��N�ff�3���'/�o�J���8�܍����B,������|	�_ءY��+����4�W9��sȶ��1�>7u��˿�FqH��*�wk�@��Mr��Cscr迱\;d�y�ZB�����_��̑8[���f�a41�j?�;�{��`���q�����Պ��A�f�c��Mğ� s����!�|��,��)Xb0_�{:�Q�^gF5�/�Ij����H�v�_��o�67�h�a/�ꝫ��m��ʵ���4;ax�O����n�F��?k�G��D�OH�$�I��m���i�%��-v�����ZC����-�M���T�����̇�D`�o���U(0���v��iSm|�[�/��9��|���<2V#S�*������&�%�9�x�r*�I��P��{s�F���+�)1�C���f8�d�.	^a7��϶�<驕��+�����(b�:�dT*x��؎����\�k����~�hyD��ȶ'���Ҿ�al��n�[���j0��	+N�N�-�T>���d��囧t��t�X���U-��r� �	��J���b��i.9{ ?߸��y�A�>PN�⊊�|���SD����&"��G�V�!��ٳ4yry��8��ft��|y�`=�q��S�*>Pf�~_m�h�Wu:�B�pw��T _�80	-j{lzj��,�����ĺ�h���ގ��#���o��i�y���yb+і�q5��;��A[Ң55�#�w'�Æ�j5���};�om����߈g���c���0""�Nۡ \�c?�,_$G(&]�a��
ds�m��U���v��o�Z���7&��S7���z�	Mʪ-���Ϟg�ǧ�����'9AAy��\4���»6�������@��9��yK�����h�Ε�\-i���+��E�fm��q�j�-C֝���#b�I��?$lu�!c&@��(	�pL	�����/K���on�S �n;� \�7ь/H��qtb��:�$B��ύ����� /B��x�d�p6|9R�'�F�h�w��⠶ku��d�!���������o:5�T��\��7o���	Q�����'X�%���$̥#����h��u��� p�+��cLA���z}$4�lY�G��mX��.������<+Nܝ�$�F�.�nmJ�/��.�2w����H3t֚�lBo0�pðn#�8t�Cϼ�����q�6�J+�������=����:��Y��*��x^�k��f'���0A�,�V�G9#����Gp��M��Y~�O�h^qu��h�קul�c��]8������=�]�v�Ydd���^��O�F�Q-���Oo+���	Y�u��Q/��y��eY7�Y�7h|:��l��|0Y�@�'� �䬥(sy1}sZ�k�.ٳcx>G@k�����v8��c��u�SlN2�l�E�����i
�����h�m� �5.$k�>��@�]A��%�=4+�#,|:�wR�gݙ#M¥�&-��,P�g�]_��{{=>�;Mhf�OB�c
���h�o"ZE�� *��}Ru�2,r%:�%P�l�%7��\��xФ��U��Db��Q��莀��>��O�1�ގ�>�[��`��b��6,�G�y[�Z��3$$��j,��/�OO3�Lq�����Y���Ǻ�q������H���VR���~�������x����)��N_б�9���#f�WoF!�j[o�*&�!���1����H]���de�o��dv^J���B���x���
���9�*���o�m��:��n�����U�+�ؿ�k�����>�J�;�} ��Z;��O3��X������&�F�9��n�Z�'+�7�>27b�v=a�ځ�y]&.��ң�7����{o�u�s̲t���&��U��qt}aO�� �ڋ���i͓ak��:�~��Ԫs�򬳹���fj4�w���b������;;�t�����?� �h��ex!�$يY=�[?���t�fv�_e㤝e���_!��q
�d��"�6����~�f���Eu��u�],��t���Wց���!񏿔h"p�+�WqS��c�h�{h>R����h��R���"�	$�� �Դ��1�$�FPI
�!���zpl���,,�~M'���c�,��v��>]q�u�����!CWm]�g��Lkρ��u����0d�u��ճ��t��>�x�tU�n�̀�/]0�ʲÇ�A ��,��AR��ia�����V×~��l��O7u���X��t�~$qцk�>z�M�����1�/f����v/xN��ŏxC�v�Z��ӝa�n�B;��3����jt�8�VåIq��J�����a�eP�U����������K��D][4B���E�����>����c�I� _��.��l4$9:ٱ
��7d@�?�kK�̧L�g<�U�d��D<���Ku#�+��u�ٝ�����0����*S�N�W����'�&(=-LqiV� ��U�N�<|��p�-�Gu��uyf����Q��|e���7@�ψT��w�<��d�<�%�ݔ絪��-��[�B�h�l�6T;�9�ݖ�V�,Nf������"��]�U�;�H��j����kϱRj=�2���Z�Η/����X�U�{��6Y�{?��1�u]�ͱ<��b��1�[|3oA!K&�V�Na^���.�wm�Y,۴��d�O�'L?'&$3o${�]H��z�l�jDɟz#[zٶC��B��A�5��mG\% cҲ ~�9��w63�*���Z�y�@Í�����{�I9��?\jB�l0-;�ܟv�����$}N�8,{�g���M��[������vŕh�D�FWj�c8߼]l*\6�--��V޳E5m��Wϯ9����O����Ca��z�H��f\f���|Ə�vp�vg�,v@]�*Eo���Q�����Y7�(��h[�a�;���#��
l|���*x���3ҧ�f�(g���ϋ��*���5@�����^���=[���j@B &��t�g|���0�օ˦���w
��e Q�k�7޴Rt�
�>'�?�k0�,�ytb&�I��ص)�h|����|�\ޑ� U?�쓊�@-&��7��SG(�"�{&�M��Er� ���~"��������S�O���["��
���Q�$��W���R:6�a1	Q�GkKd1��ҨGX�i�����dz�<�?}��j�네�60���b��q9����B�?^(�$lSE�/Q$=��*��9��o�P��i<�ȼտ.�d}�ϏL����5\Ȋ2%S�k�N���Q��N���h�z�lޜh%���;^���p2s=����0�Vg����r���8L��6Cs�a�`�	�]�p}���Bu�G<��ϝV��'�uE�PM<���0�P3V��2`��_O,�R����[�l�4�l�x��5�&�AI.y���a��BdO�l�'���Ξ����d�4��Х��S�{q�-pq��U�2kw��+�eJ�	�x�����2���t���y�e� �v�xS�;f�������A�4HE��`����\�q�<�6Cu��8n
����v4~ϊ��tƆ?�IUy���X�%d6냘�vS���e\��u�=#��f��;j�۽�RM�V ~r8���֚Y�)�$�zf9s��t�b1���G1���G�XO,�i��qc�z��+�>7�/����6��eԶ<��4O�%r}A:a��ɬ'����[�.]�"ו�ƭ����ۏd���?����F���,��˴��Gڿ
!=���b��Fƶ�@�m��Dd�m�E��*4,\JH�U_a$C�C���F��ցJ#�~}�t3��\l�������;��5�oͥ��`J�J;#��˒L⩨���~�a�9@n_���\ч�e�Wa�g��	��)z/��2�7���+�'��W�ipj�Xo��7�����+M���IRۥ�|�!S�j�k4�K1*��~M��z�SRX����x`@O ��۶=���t	 �Y�����H�h�^�KQ�X�s�U.M�\�~�I�������b�����)�Ñ�q�'��e3B��@��q\�V�~�B�3��-B��iYֳ�kQ�����B׳����[Ow�A�hÊ�������;6J�����+*���4h����)]rk�Wye!G�Q3�F}�2��װ����qa[��t���,�-s �i0b�˙��������⿎��7�U{��m�Y�
Tn��@?y٬[�S���'&ҍ�#ភ�ƃwD��}�T,��|��^o�ָѐ���w�7�g��.;L���Ĥ�+�8*�>�G�\,�TԎ�� �͚�G���)p��Ƣ-+����o�~0�^��ٳ�EI^wf-�z��d�g��OM#�{z=��w$��3�I� �t�₉�t�k��/��l)u��>�������lNE��;�Ƕ[Y��Z����𹉞oe�������m�@���Wh����Z�I�E���ʮr!����5>+ڊ�OW(q��z�Z�2��P�bߙ���V\�_����?�^�U|�e��1�)�e�,��p���k#���>�� ��VE�c�'=�丞�O"��^n-�d��wc5X�3����@�ye�@�@�|�+��Nm�p�8�Po�����ⶋ�ٸ��Eo��m�k5�xxf��4��x�&��jA��&,�#�b��֡�����R�,V�r��R\,	���3��Sg�6��<,�b�7����>��GzI����=9����m�{״�(a3Qz�`TY;}8�PFE�@lm1�Ԝ8Rg���� Bj��]�Z&Z}���Q&��.[�ևBy_w|Ώ���2�>Qx���Ov1���k҂���L���lxFىE��9��sP��f^h5�>|XcN�R�	�9��H`R���Z-Uz�w1�r�ƩϕzhF&�r=G��m�>=�"ڸ�UM��i�SB�Y�u�̑�����7n�&��IH�d���� ���o�֩�������3$��y��쭆�s#�7�&w� ����X|R����i�)T{�D�[p;u��h��1Ҳ��}�˪�b/Y���i.���w�j�����Z��ּR��� ��nJ1���gEh��ع���l}}��h���x!pw˯H�d�'��gr^���\��5ú��hea�p��Y�/,�î&��8�O�3����|�O ^a��R��ζ��NS��ǖB�6n�����T���1�g\{��N�	U��i���u�g�Nf3�Tد��$Ow⩙,�O/#j8%J�W�7gr�Q/F80��E�ބO��<���Bw6Uq�0Eu�ŃK������wc�oD��ģ�:�������Ѥd��HG��B1c��
�Q�	��=���;���^!J��7>�&ҩv!Eȩ��\J
��1��J{���Bzj�\�G}M�<�5e��R,v�b9>�q2�k��8_�(��Y�}Aj�~"20֑G!.L�P�|��'������� �೺�}Z��\��U��^b=��4d�V�d��yo"��vXWu]�-�d����].�e�m����πc�6=��g�їF��̃����yҋg{�\�a�k�{jj��Kb�_���tB��v�����?*6�`���G^[W��?�7Qq`��U��(���e\����@�\���K����[��G����M��Cy��[���/�{*`���`ۯ����R�?5�ǊP�c����ݜ��$������0���~�k��\$�V��7�B���	���{u��~߶�p�Z����?C��$��սCDl�h���.�(����?��ظ��؏<p�-Ev��a� �c�r�7�7a�T5�hu�w=���5*1�f-|R�oSgS#F�a]����GVo�ލ���M�R̉B���ʡ<!-	�1^ه';B`S[�a��a�"�c�['钢���nw|%u��0d�)`z��r	KK��<�q-��ӷ
n�<+U�����E���~���_1��3^���fh�8a�C���2p+��r.��p.�X����}w�|S� 'b-Pn�z��q�P~T��j���"{��Τ"Ԛ�ϔ�!>�(��3�lg���P�+ �Ob�������zl�~^��5/W}V��"��P��sJ,U���M��~'� �l�%�%�T�Վ�=��D0��T-�_[�f��+��A&����DQ��%֬X**b~��6�����)Y����@ȸ%y�����z��5�7�1#)�U(ˏ�;N�5�������sz��r�T�ř�׃ �w�BJ���e��Ʌ��6'��\���e�hMt1fH���&7�y6���<#2.F֟���eUJ4͞��č���t2G��v��tF�c�pɁ�"���87x(k:��U7���ѳ�߶�;rig�ٜ6��yJ��7aR��dR�}8��]3� _�Kr��]�%2giVt�mo�Er�S|bRݔ�2Wuf����6,ӊ�P��ۦ�t��f��)/�).swU�����l��Q��2q��z�����M��}�<b����Ҭ>"ӛp��ٟc������
�&C�(s�_`c��ƾ~�)#.iq�:]��.�2:�"�K�&�����V������^��!K[�/��������|���(?a�e�㽨�3��痃7u�O��-[���/
�]���N�D,���L���������N�Rݒ��s�otˢ�az�g'`��7�[s10�0�^���%�6�f����唛�kG�yA�B��nL��{��9?|��¾
��3�z�j]fX�W�1��m�	G����n�M�& �#�����.'6]im���3��x�x�9F��"��'�	���������������N�[�.�61��������A)�7��4�H�ޮ6|(��U�������0����PKL�h���'xƴ�4�ح��XT����՟x.DOb_7��<���Y��w�]��#)�*���Ȼ��;"iw�t<|1�J�	����6{��N����)�o�~Q˕I�M`i3}�R����||�N[��<^��ں�l��d²"�
1��˸6)�gP���XF�#~C��;��PV��W�D{`��'�>/�C�t�`�N��R�u�5s�J�zq��R��?_�3ڣ��ڻ�-����O���c�+�~�4�*1G�x�s��nb[�%a}�U�ή�.wW���ܟ�a�:3����+���81�0;6{��f�w�#k�V)�)S"�bw�~(�u	AkE0����{<}H_xMC��>�)�"6Q+�pwc�1S�v*�����A�.��c=!�2��/T��Ghr��>�İ��q��5��^�ٵޡ�m[���x^��]\���^������>JP,�DxZ=��,к-UXH�S���A33�z���>�!�.u,������q/�x�f�׭�@�H4ad�s�Ն�� ve|���#mQ9�$����hU������B�Wi>��l!����t[�N���#S?�����yU�59���A����u�{�r��9xC��|��rܳ��=��u?�g�׵�ƿG���P�C��8W��Y���~|N��'j{�ߨ�4�� �t�S�Ğ#%�	S���<�y�>45n߭~^�JyfF��r�k�j�}H��f��T�j��χ��Å;J���i���E!�{bl�'�lat;�uY�~�F���V8s���5����`Tw���Xzv��faH��W�=�!PB�GM2�-��-�0�5��M�b�	���Nr��'^t{u�!�N�?�u	� �oN���� ��#|SS���������p~�
�`�QƐ���ɘ��#�; ��/���{�9�p��8?��g:�����#!�_�\]l�S���Oi���b��7�unq���7�Ӂwo�؞O�N�~;�R�Jr�~u�R�{�߂S?��QZg=��@2�T}�H<�B%�n&������$x��U��2�� 8�������Y۟��p}��.ax.B״5.��t��>�UPsC�I��3�ؘ\H�U���b�\����9��\B*j��{��"���A�a
C�.�ߓ����N�� ?�x�9D*b����jC��V������)��ު�B[���bdFMD���Я ��¼|U<WG�o��QZ6���uq�$�>lAL1����	���߰��~�~8���X��iB����>�������b �*t
"y7��c,h�͐K;�N��*5�6�F��6�瘑'�G��p��7����p�^Tq��9��@(�F�1!"����=����hL���ZG,�
����L��� �X����$���:�^``��67�`��{TIr���u�qv�N�s��}�J�Er������
�w�����2��T�U+<�r)R9^�!���p�+pŪ{���٪��V�$Xo�]�4�K�dǘ�y���N&�N5�ߛ�A�K��1@�@����}s�������db ��t�F7��}l~Qb��@\��R��:-�~���ۧ��5���x��YJ>������)v��B5
�����fu��Òe��
K�s^�:���f� �C��Yu�#?���&�|��^�����X_+��uA�xw�M�R��ÚwϜѥX�Y�ؑ
�����!�&l#�S�oW�� )��4�EI�fB��D�+�g��Rm/�ͬ埝!�|(�h�zj$ҁv�Oč'_�g�$>�N~ٖ�X'�#)��K�}��}.j [�3q+�J	�:�[���Ec_\+�Vp6o�0$z�^G�k���5n�"�<!6�)��?w^�&�����s=˴�`�i���A���Z>��~!wl|uݲ�l=���[��q�������d��s��[gʌE$9�ۯ�l�,�sM�D'�ײ�Y���?H `�T��໽%���m�mb�V�u�s�l\�a�o��L�9�|�Xՠ�'9/yS�v��⢲o����ұ<V#�!���4�S��EI%��dm�����FrP+�;�+B��⛙�b�t���غS��cOOW���6��;Z��ݲ}.2��hJ>l�w\�w��mw�H��}�|q�P8j&.A��B�k����
��S;y΂��,�YS�c���j@�R��
��w�T��d����~Ó�E8��b��s�M*M��o��J�	o�{P�۟h��/�X?���������z�b:�T�aE9�?���E��߽ۏI־��!QP@�J�����;���Ŷz�ն-�>�In�[;f_�*��p�_�K(o6��*9\��`}\�b�RM;����x��xM=�/Q���m��ra�k�@X���Cl�8k�C�[�2Z��gM��R7�����H�4_��`]�%7�U��j/�~w���H���a\�oG�Jyc�y8i��C�j[����ъ�Pm5~t��z��nK�e7Zb}	������
�ͭxq���C�\LRh��v��4m]b���?h�h9y��HYF�ϯ��b�u!�]V�vaS�����K�.������.�G+Z�{��%T��J��JK������o�u>m�3u�O)�	�c�͈	u�� i(mo(�NbO�^d�+}�x��0�N7�U�oyvE�O�f#�R8��%CE�G�+mUu�ӌkъ��"�O�R��f��1G�d���������_6��xR��2�{�ǩ��;���70��ܸ���\f�cҕ�=u��h&��������7+!�KGF+���t��Xb� �O?����Y�47��ߖ����-l�qg�8l�K�'�U�/�-l&%�[3�����4K��'k5�k�R���_�d���'t�s"�M"�zh��a�����÷?o�ƥ���)1��0��4�r�%�л}�<Io�U�e���~�Q5����"k>_D�J[-"z-+�f�E��Cw�L��1W�7�@M��`�t� �~�=\i��RX�ۜ5�?�=�w��T�p#|g�=={�}����ˋ~��1�^x&o���4���j?v�w�����Ռ��H J���~���v�H��O	�o�l�����8�Ib������t�Uͩ$����%��Cw?C�b�xq���|�-�E���^�Z������ޙ�?��+}"����ہ���A�6\���s�iB��k=�K��P�6��Ћ�b�uqj񵂐#��e��hP�@4U�������l*;���n:��Ƿ]j}千�~�������h����K7�c��T�3o|z�� GDzg=i�7A���"5AW��TQ��;�㶍/NQm���|ᦙO��� ,�S��kQ�;������M�'�>}Y4���Go�<�A&�p�L�!p�����ז:�w��_z/�g��&��t�+��5�d�R�FC���YH�kI!���A�����6��of����K�Y���	c�Wy�\0{�N����p���0�v�����80��KՊE[�Lj�c��h�.��X�[�8�mnvs�6519`� A/ �3�:�J�-��Ӻ�Ҹ�u�\�Oe����_����H�55|N�+��ѭsC��(G��#�)_�<�4�ζ5YA��m�����W���������!5VOx~�t~���يFNK�E�7�L��,�:#(�]�*��J�o���|�b�q����4q���LA+�;�> s?~��N������ؕ\�n�R��J�enCto. �2�;W��=�4���R� �zk˃��bO�?0���F7���j���lRǟ��8��܀@0ROv�9~+�8�-���u��c-���õ�6�#��f\鋈ڛ���l�^k�|�T�}u�Gz��S��`��[�� ����z}��i����S/��Κz.a\��fA�j�6C���}�ߡ�߉Лtݰu�\a�~/j��1��o��mfM�l�����d�vrdj���P��6�Fb^�~��.��'�|:��h
��?�����h�3���9!�}�pz��zN��8�q�V �i�/Yf__����[;�K��W����S�����;6�Ø��p�\�M-����-!z����I�Ñ=����7_>q�c�=Zq0��� 9��8�Qy�]�u���=;�m���[�;�x�Ͷ�<�5㗻���,�J$qd�q뱟*3K]J��ħ<'s���䝝wN	^�7�ay=�x��bJ`4G�1*�<����Ъ:���C��D�tI��+��/҄YG��c��U �����n��ʝ�U��?�eP]]��l�,�w�N� �]6�q�X��������ٸ����;�o�{�o�����U��Y5�\k�1V��y'�B.6���FH�T�\qb[}D���x/�|QǵO<��y�c,?4��Yܑ�0�F�vﮧ�I���eY��]Κ��HR����J��3Zc�{^���d`�`�mX�w��\<1�"�J0�\%�qH��sAl�Ѡt��w�����81��&�V�;&qNϼE�<��%�=��j��ך/�\���ޮ�VS�-�.{�|^�"�8�ɞq�K�G�gP��#��=�1i�	�i�8����7(%�,u�e���he�e�U�?��be�<���}�&y�>�=�iȢ(@5�-q���b�� 2W���$���f|r�S����.�q͙��]4v/xA�!T�ISu���;�� *=���T.;�|kx(J_>H͞���lo�?� j~D�uyW�ɩ6k&��K0�DOM��1����ѐFq�rQ5I�bb{�d8���2�z��^(9�<!�#�i�D~�~�tU#��J��|��w�ntt"�����/M|"y]ҹ�:�(B��*|�r���ۓ��G��F��l\6�% H��N]&����}�/<%����P������	W��w�ވ�����C��� ���O�<&��j?C�dM�M\/�U?ˇ� 0�%�sk�ݱ���I��[���j�q��T�/^v:�]=U��i��1���� 1%쥂;�uT��ՇEG�J���\Ȋ��B_d�~d{�v����ɹB.�Z�׎��u����-��E�Ɗ;l�N�DWqo(}��$��!�j3LI{��>5�$�`䂎fr^Ҍ ��]��,�'@��*���5�}`Ki+����oW��57������E�{"������>ྔ��Y��mY�3�a��F���D���~�������Rh�Rs%ޏ�T�n E���pi��M���GWjǗ����d{��;G�QC�6V��O���l���z��E@m��ė�vV�X�>�x����d&G��]nv=�^��O&b�A����Ik�][w�[�x	!�����Q�ߖV@W�+���X,���z�A;�;R�l{�Ƴ[�־��}ow�Wp86�.�e����Q�Y���6<~�[)���Cb�J��݂M�-�����{�|3(���f_��xJί�kZ�q6"�y���^��[�j�$�Xw ����.�S�S�t�]W�b�vU��8��o�x�E�����˜�,'_N�����ׂ͙6�������<�\�T�%w��T4�}��	���ᎶN26kƌ�뎥���t�� Z�R����-��kP|�FRg�q��	��G�P�֣���߃�iܞo��꿫�S��)��`>�0~G�ɰի�?I����]��Kޟ�n�QP��g�q̋�-i�Y�8�JxQ5̙������������y�̊��)ڮ���![�D�Ht}#�/����2��~�n�x#�9��إe+�ug4؝��h��7�>�@�[���)��[�f�^-��ޛP�IcFb��Kxy[8a�Рa��3؜�S�W��8 �vIKߪui�p[��'��o��r�;��$ľ�U�S�u��Ř���e�=VO�:O -�jS�f߶q�������YSݩ�O3<3˝���\���L��7�]"�qt��X^u�L�r���P��?w��G
�YoMΖ�y��>_�Qo�[��ij���/o��x#�����yo�+Z��>�іGbS�=�]C����k�<�؟��w�ufG:�A^1�D����D_�^�C�d��e�����c�o��T���I�p�����\Z�F�]ԟ(��뒽���pU�ER��ki�8.%�uM��>�w����^.���8ڹ�����|#1@���T�$�u&�h��`y���7���k�p��O��������h�}�#���iն������bF0� ��~5�#��w�wh��[�	�W	�П���c:>�e�2��#mQxn�[a�q�{X�1���B�#q̠���ە����������{�=�o�6��y�u��z�W�uj9��k�L��r����l����Fgd�o�5'�{�R5H�|�$��o��"/,��|�*�?����!���WRG�Q�_I]�K2�ܠo��:���j�O�f�s-S7���!�/���7�H�/)���i��<�ٗ��_�^�i/��N����>��F��=�$���w�E�w�Wa]��H)�����a8�)�'ؿh�c�)������m>lbih��5�������+��7;��A�������NJ�E)��bH���1L\ݐ��֐�g�[�������P^}�/&�\*�A��}����D6 ~��E���:�����`��H;�v��4�>B�)��o���1�D�=�O����U�/f�S��*Ycr$�-o3��E�ޖ�=!.�����Y�a^pD�S~�]�B��� �
x�$A���	[�~��j�����ޢ>�PZ�R��C	��.f���>���	b �*� ��ќO����D��I�	w}���}ۃ���AȗҡڿIEh^(VrU���M���iT��KOs3^���X+�L�do������H^��#g�i���	�d�F�Ф��W��y�x`o4�DM�Z3󩍻�4�-©�ᐫ�a�7A쪀"�z��;E�au�\1����az�'��R)�4z�A@� $x�)���6��Hƈ)���5y��bn���n��T62����d�!��2&��eD�|d#���J�5�[���	3��$Av�jk �6��kv*%9 
���Y��e��s�C� ��+�9�������j1{�F�W�[�c\c
�;8��9�̱�s�����ظuϻ�A��3���`'J��Cw緎!wa͓�fx�j�0���ē�c�gð[�%��*<[b�4��`��z�K��w���*q�CP�6���u��	6|����3�cw��e��׵��D��hH��_�_N��M�"ќ��f7򁯑%\<�L�5/�O�ܟP)o�N�U�%��J�&���$r�qs�>	K�6hz�G&���#hH�r�}q���i�m�e�)x���3l�,�Lt=���	�GxH4j�/�£�#[�u��D��d�e9^����b�x&�n �и^�&(NFoD���qЉȮ*��#Q���F��q�^����e$)�`S�
.P
���z��9���a.߆7'.4��7a�mo��V<'KI`\�Rb����|���JJ-�	�O�?6mz���@��>"���4� ��r�����ر�f؄�l��q������i�|<"B.��(�����{A���z%�t�]�
XltX�J-���>$#yfl�E�U8h�o������\�ۭ�C�@��i��P�U��`�����Dk[v�b=�oI�iy��B���K!'w�0U��'���s��O��O]6����݄�4J��H�N�'�D�qZ��'~s�Z)B�҈5aR��4[ڟb�?�r%������<�O�6�h5�nߴ���(҃/�H��dW�����*��##B4��"c��<e�BI�c,l+��{��.(y�q+E�C;/��u��쒳����aQT��JO��SJ͗b"��_;/h$U�.;��K��\Ì@����*R��D����5(��dޯx�i���H~o�]5��/�W��{�+�q�����(�7�=N�+��v*}١��;T-�(��f*�����|w�n{�J>6MQ�(������쥣�$F��Xw��1�W�;r��v5�s�2�%Y�n�Le�jb}7-G��YT��{ATR�&��!mb�I�S�79e���D,�"�Jn���s� �.2i�2[�n�;�A��
w9�VJ���|�'؃h/>^AU���j4��?�׀S��`%Ct��Јc6�[���@��0b2�ꪂq��!�錥+��-����bZWܨ}���h��7�W���������x�z�jW��F�j�؆�ԗPUe�b|u8g�?n��O��hFM��i\w-,��� �r{քB�%k�+Z:��h+�P]��l����{������AX�l�]������:�Tp�A�� w�{�7Q!MnH�{���6g�Tt3���pz*��s}s5\('���g���_�l29���@��PF��,$��</-��g~3�V�Js�:�-�j^�T�0f��Ӵ�!��<Z��	�Ax?�?�U��b���d��:2 ��p�)tl��~�|�@�2��R�& �DTG�Ade�r�s�.vMeQB��<�,�һj�����k��<�#FSȪEN��K+S�8��|�ę���� V�d�w>_+	6���O�n�wa�r��p�C*���>'".)v�W�\�@1$�k�3�QBdjig���� �Lw=�D��3��N׌΋kG�i�.b��R�!x7a���PWZ�ux� ���5���̰^ߏꋯ����	]�G
rk�H���o�Z�3�s�H��p�2���7@e�h��;Jlo�;㻻�����K��I����kh�m��%_Bu[zN�a8 ��
~�+�����s�=q���c�H*�3>�Ȼ����W�Zg��~�\ ����긊�W}f����.�_�r���{y�(��]�ڤ�)E_�A��~�:%Ik�k;���T)87W	<�DT34�s��@3Nz	/�e�0����$�btv���Q,�|��ۺ�����D ��O�_G�:�.�̘$�K8�u��dz�`��
���a���>Hx:C8�������6�l�ꭆ%�(�H���Fa���a��$ٜ�ݒ���tvIf�4��^M�<xt��-�������Rё*�� պ%��ú#خ*�dN�s�q_��bň�rB�>�*U��� (DvV����	
�]�$Eo*�� ��0hd�Ex�R��^���B9?T˗�ġ�;�}�@s�����h������ӑi)�'u��|a�v��
���"���=��wvKѓ�CU�GƂ��_��BRˏ&jG�C{���^�R���|�)�SC.�X*Ɔ�,;�1���P�ξE=:�];�ic2:����� ���Pkj_;� #Ah+㧥�%+0Md�yd6Fz�J܏�%�Ku�j�V=��wY=��lm�E_�u�*L<�ݖ��@;�+�Q��S��\��Qd���~���/��/Jg�2\7�d�V�=3*�p���54j1_�Dɟ�w�7�?p�堽��k��	�@��=9;`��E���,�k�A�b�4�E�	�3���D�{�C�j���f}׳�0�6M�@����<���SBg�HfR�$��y(��
�Q �C��-�&�cD�b�:��?c�K�A���%��U����B���卝0!q�15Õ��Y��������)��#��(f$�ꢁŤ%�����o�{����
VsM�/]U��կT����M(�t��||W� ��m8�H{ȥ�0��~��l��q���x�� �K�e���@t]�W&��S�V��;�/��&���\�=[{`y6�%"�0��
�԰	l�Cq��Y���[�&E_;Gb�Y������j�����3��O6d=�	�(^3�j/��
!��<%x�3���2�!����z� ��+y'��=�Y�^b,��CG;�Y�I���Rv0C�)��������MRy�U�=���k��g�E�͘�ɓi��ug�g�����T� ,9��c�q�|��P%ʓ!�sq(��b�WmI����-ˋc����SC�m�'*�潨�z��	�Dq�9B����1�u1E?�k�����#]�u)12O��F�Ɏ���2���
�w���N��@�/$\ͭ�CU�^u���/-�N�9��h�(C��"y
� �?�r�<tR3�X�Qw+� P���O+#y�5��̼2O��1���iqS[sC����X#;���՟����՜�T���&�lŜ <��<=C{B�%A���]q�aD��CGe���g�k�w��;����m��Q[��O�M��kt���;><t�BT.��0�:�a����{�������IϢ�DRQ�!�q���Mk������R���M+B�+շ�����#+8e�1���l��k,�B3ä�hBqs�}���Y���&<��v:v�L�|���,�<��55��rI0��%��I�c.?$y���\P�x��J�x�$\�?|��"����W������!0�d�fV�x+2f�MM�$Rp�*0�n�\��벻�Q*�k��**�
TxksP�$�ӁE�t@��&yJ[�U�c�(���8�yI7t@ڹCԍ/)4����[*�Vٟ3�B���dJ�u�aʠ:w�?�Fǝy\�ݏ��y���w�|�������^�-ѻ��p�Fn9U���H��iX�PSe��XB�<�3��,�Э�eiQL)�����rN9x����eЗɸ��}�1|O�D��N�E'd�t�bL�(�@Ψ�^޺ݣ�`��k�Ly���i��W�Fu5[��\�O)�o+���u'6�@��O�{3X{5��RȖW�.P�w�r����UՌҋ��~��t�g;�7A�J�T�m�E�f<b��(��#)OҋO���wcއ&n� CP��gN���zO�q�k:$�^.𙽊?K�z?�֏���g��Ю�_M�Ss??OdB�7��f1����m��%8�*����o�-����%5ۢ�>s��x,8��?vd9"������U6'���N���K����3e��(/o	Q����j�'):�	�쑵d�k���i�ńws~]� h�WʟvC{��$�j��4��� �Գ��v΋w��#_�^�K3�P�?�侃�F�ɍi�{��4�8��B	�7�4�,�G]4��`��?A�@E^�㖨j�1��eA,��n !�l��#���.u���O����O��? ��I��G�{d�o��a�U3��C�9�'����ϣ��d~E���kz<`E��f꾝�8h,ࠡ��[�c�X��b����ʺ�q;&�巎�,4��6�>�&�sM����5R*&l��&��^�����T�O9�Y�~u�;<쮌���ͨ!uM���])jGv�g�@��H����u�1�q�|YD1+[/�idw�x�����|3������>��h��l��.�|�~dtD]�W~*H�/M��S��/�Rc��P�"1�!/Jp���7�1_�Kc�P�&��-#���1�V2S���iYO[��ovd �A�^��E^�; A��f�^��~�T{�d�"��A<l�o��v]6��#侲7��`n�g?�{�P�I}\&rm:���2(u��k-��T/�y��'�1}=����^J"�U��q���i{�d|����51�Dy}W���g���m�D��4cZ�{cw�5N��"��<���e�4��s3F�V\����Ud�/�ǿ4v���lS���m�MP{�l��Ve�Ʊ��o�A��1O��t%��\f&Iؠ5��T��v<���ғ>غ��qn��|J�:��)���mB}0HԿ�m=�Z{��o�-�1���_�jP�nh��\p)dt�褜y�3s��h�B+�l\�i�Y����窷Sq�7�a�k(���Zf]�5����}�A��8 w�M&�����{�FYe�{r�����ZV����=���e��zyZ�l�����w���m�u�(I殻W�/
�Yj�qZ3S�5�7����3~�	|��B򣃞���:3���'�&�_l}G���2z$�D���QZ���Ȃjf�b�|촃ę�&���@(y#�޶̹��I�Z��kIr�%b׆����@���s�|}�޴�AG��aY2hM�3�� ��U� D �����9S��b�TYIVZ��C�����Z�oſy�V6R�������wl��)�x|W���X3����|�	�l�yhHM%�7�K2�ߒ��U//�ꏹ�u���w(!��Ҫ�����SIz;f��v)��7{$��!��~
��s�0|������K�[z��o�Z��EM2��~LӍ2,[���-l�+��_	�Kb�������T�Q���4�,�D�aX��Z�i��H�kЯ������u���͋/Ɋ܄��;V��1�()
��]P����0%!���N�~��9�D+D7�HK�&)�@Cq���B�����ؗ �|����n鏆	LP�~��-�g�T?�Q�Q�O��SG��!c�fȨ(�B��i�y��&����`s��̎#�]~}�cKY=1g��2���#��Uh=�x`��-��\$�/d��0��_��v�dQ��7�KIz�eغ�M���vvT� ��Q��y����Gimi�J�r@�p�l��kx�IM(+y*(P�|О���nSk�&���QT6F�˳��y�f�C��I(\-�x�E��|��?�S��`�>V�q�WPy�5�`�CI^��V�;Z�Y��}�Dr��!��n���&��;��1/6T����-��L���6�5�=��﻾�X�E�#}��i���7��=P�^G�x�rl�Hlm�MK}&��D�e�N���ͤ�=�fܘ��>�,�~���!tj@YM����v�af�����p�=��F^W8�.@2W�a�e����M�x6�Az��)\z�y���a.g�dKq����;r6�pB�3ⲩ�g�RF�ON"	�ކ�E�:�����޴�7Յέ��h��_�Nn%LF�U��]PM¯%�Cư��(���U�E>�Yu�%8VΥ�/���׀J֥�&x�KO=:MD��S�z�L��4��.��珉:�˩�	�C ���8�����'����@��j���e�P2�����-'Aͅ��v9��[�<;��Ϛz#ljb��H��"�JEJG���2����j���,e���Z�&�����s�b^��������W[�>��o�9��Z~���@�;��T;�2=�8؄��jWȇ'�$����e]����m��rLAy[���*�_K�K��`y�~�U�M����U��CQ��cQj�r�ߏ;�p�}���N���s9�l�Ԯ��Ȉ��-���_��L��*H�d�e!ә%��s߇��Y,!4��*<�9��c1W\�#���i\��d���=�v�ˊ=|�"⥘|�a���ZU��j����e���F���#"�H�n! ����T����Ю�׮�(�nwB	�rΊ��U�ā�>\2>E���$�P��&�����rd��T��.Tn�G�j	�A�$a5��������xU�f��V�_z�5��i��#ԩD�3c"�T� j��������9�1!�f�z
A�]B�Q�C)r�ot��uք5��c���0����>�=ө��Ox<���{_�&��g�m��?�}�qڿ�[^�]���~�8u�Ҙ�r��D,@�tq��$jTE�+��
¢�Y���a��L34bl��^��m9i�J#��=��#����P�!d�X�D�?Q��M�w?11�q,m䌽�#��6\|���B=���p��qpb>�ϔ����V��'��UwLW3ؓ��"��2�bu^�z>�����gh�<<!�Gט��:sf��S�Y����,�;߀��?ct>���a���t���BbYNq���F%!�oX�a�X~�i�ۨA5O�L���d�0���t��s62����dέ6����x��(��Ƚ9k|�����#c�F�ě��o8�jIKYt-4��w��T%P
��c�ڸ9'Wf[t�^'??��K~ޠ�5����D0���E��ڕu���>}�$�X�OX�t,|,@ཡW/����9F0|���@]�����n8e��U�#�EݘH����4��]{8<iy�x�=o�޸"�$��▫E-xu��*�M�h`�r)a������	b�l[��,�:��%U8�Ė�Q�"Kdom#���WHF�7��鼹��H����|�~0�ڏ����)�����u��]�	���X)�=x���T-؟��H9�?UԹm���˷E��}���(y��û�G����H�c��J,�m���������؂�-w^i?� ���3���@�錼��,�����0�(%�l�Th2\m��@�y.U���C�5`�(�P�3�]�����@�y�2��z;�M�C�5�� ��q��$]D0�n.x �b���~&e`!�#�s�ļ�Iyd*<[�HQ�]~�R@�R��D�S#F��#�3���&�l�Gq_�w�������K�xzI�v9S�<��T�Q�ZoN�6RD������r���8��n����v8e��i�%E �d'Jq���_���)�kj4���L�X�5��q�UL{��N'�#���0*8�o�
���� CX�E�CYdÜ����g�W����X�$���Rf�p��y�5Hq�$�Y���$-^��'Mr-W���ӿ���p[�8�XI�*�$HpP_p�V6���t��Y���̳2l���NC*K�vtlG�%�u {	�q�;AM����*�v$�4�xޖ�ݑ��Y���vS��q��U���Rޫ�:FBZ#����{�5��9���ٌL'�]5�9��ą�+����
 W?-��\6f,��]��3`uેɪM%�e^�:MO�6L�_�'����>~ҡV5⏼�%]�0u��I�t]��&;Cf�dC(���ט��8���M�a�p��
{:|i�߿ĵ8�|\NW��n�NC������:���\cp�B�:ɺ��?�(Z~�0�Մ����� 	'k50:�g1͵�$���[A|nh�!�X �d�s�c���6�z5�Aه�Tj���|G5&���p�����L����RU~m�D��W�'�$2̈́�������Ժ'8zޛ�kύE���6Ё����r�l�'n7���z{��ؔ���-�Vh)2ϕ�8���I>bi���ҋ����ǜ�mB�Q�a��7�P�C���E�ꡐ�JL�l��0/l��
�)u�W�l�^c�c�A*a�����:���'�Ƹb��d�C��d(�!RD����Ƭ#m���W�9M(��\T�l2f�����@w�N����jh����)�1E�~���0�nt���������T�m9�%zUsȨ��Ԧ����#��w�V��f�|O[Q��8s�8'�?��1���?V7j�X`67�3�U] AR<�jP��h$Ʉ�4���h��c��CV޽�wP|#Ů����։
�J��ᤔ�����Zz�CP%+�-����]��f�p�jA��t�Ҍ/˹�}���}*�$�Cė��������̥���
w����Y�J|�T�^��5�N73#:������?��Hs?��ë7~^�_x��UP��#��3]iD(��@�#6v����t��Zə��*֙�Y{W{g�9�E���<��C���=5d�{'���׀�8Y��<�x�L����R� ��-������no�^).5�;m!+��
h�J�n����߰[�8�ŒY�a>�N{3�,�`�P<�%�J?�ؕ��
3{��ut����R[�o�y�%�� �Wm�sF}'p~ː������<�G��G+���X#-&�"{�2[}�0 �k^W����0�P�kD��Z���G"w�"v��-�u7�����k'�R��Y���nO~����T�U��rj��BȢե��Iݓ|;��ƨ�����/������o�l���6��0C�wG�*ũ��S�������W��K=>�i��2�?:�u�HkU��0�,���Z@������vt�AǭW�I���-�Eւ�p�	O�KL�CxS�*PP����MU�6Z����-17����>;5��M�����'�r��
Q��]>�����=1� n�>M����t��x{vYi��D�5ܡ���I>�N
z���[��R�J1
5��-�XdEv�fmvb��S׷�$)�����k�w��tp�2���h�ߘ=7^*[��꛺*D���h%��l0b�;іLS)C����yVZ�퍒�C��Ѱk�Z��㉈�ɒ�\L����j�8�ò�E��z?��a���뼒	�����V;6$H1�A�6WZ�h�!;����K���,L�.1���!!��U6�::�٦�p��n��M��O��Kg�r�x%����8��O%�9syqI���� �����t	�� �i[,��ݔ-���+��BD��.���,�)�fq�&��-���k$s��;-^SNW���ն��A����9Dա��(x�]/�R��낮$O-�yqC�k>�C�i�w9��
IMkհ��S/��YiI��Ǫ�d�n�]>F��4����Is@�k�8�Ɵ2G�.6��E��b��)>�����HÚ���~U���sI�1���aq�a��t�ƃ0[*(|�x����h�~6�yZ� y�W��G�o�:ƺ��ˏ�X&M^�wM5�C&R|�������#k1I�]@��z�+�Po�Rr|���[y��P��T?M��=��-���#�����a���w�mm��\-t���	7X[�Ίm��[���4�쎻殊��>���mu*��_&�R�l�(r�S��zeT�P���vc� i��(`���*15hDGA{K���>ex�5�$�׊M"ۣsÒFJE`��zR��taz��}@���K���Ԧ�ۈ�s�M���ìp��?}{z�e��yd����E�R3����\�9�MV��Oi/���3S:�/N'���
E��쌦��t���Y�ٖj#�#m����+�7L�n��G���U랥&�	e'*Np���y�;]�ȶ����}��.uB���P��F���f��i7 9۠�����vg��.'&V���pSQ7
�������?&�
쯩<q�|��|�V�@M\<i��;8q]�U������؟2���8��i�Lt�� ��d07�,����I'��_p�h�9��(ញN�o@l#t�O��\7T�p����@�ƥ9m�H�����?F�����
/󞾱�i�/�����m�ḚO	�;�2¹� ݱ�6:#�^�����^���p�)���@,���IL��%�<��F��X��uZ�j���\9����v� ��pML�)rND���1�ZkO'�=.�B?6���J
�!>��nD���R�
3���U,9��5�B���qh�N��#nv5����\���FV\1/9 ?��B�:1l�B�%��V3B˼���-��`�8wP�0n��(�N,=~�;���U��u�3Ns5��#���t$��
��Wm�R�f��=��y��V����ԛ��d����n���/�
�����-��M��z�8f�T�,��}ɍu
mJ� �P��vNl��w����jd�iYw�2QD��O-R� �܈���3,�}�g<b�Q\��9v�U��TĪ8�V�v6Z5|S_�j������Bn �@b��HT����T�󹑇�"�#����z�ʊ�������۔�C��眓V|������Պ���2��/-�{K)ύ8�(8:���]_����oR�s���6Uްm�l\�%u�����E(#�,��3E��'��+��n��@��1M��)�Y��������;*���;;K���w���#\��=�.��a0e�I}�F�^X�B�deX��5��.#�$�I �^i�����p�JqCu�X�{_2��7s�يR+ònd���EA i�l��q���o�Y��y��=${k�a��zX��~���{������Y?�1Ƅw��WvQ6�^E��C�l�k4��D�y�f!����޺J2�0���]��U���d�6����=�\��Of׀���QUj��:j �vD�L+��j,љF��W,Vא���I����f�@U�ý��n���<p^���6��k�$ץ�ejw�MP땐`"��J�K�{k�@���_}�vMz�����,ϻ����!y/����IJG~F���r},/���a콨N�ؗS�} � �����M� �Ֆ���5�R7B�hPFmt��)�4�*!4�4V;�%ؚ��� E3S����{�=�3�������T����^4�6<agN�</��	JLa�BzF�e*v�|�K�����6���7!BG��f�8�����]�E��+�	.�6�T��k7�Ol ʋV�C)��(����B�:dN��q�/%w�e�[~�w�<_-ѳQ~�횺ϟTX�����!�	��ksPt��x��oc��� ��ww]��O�S��7�k�*wh��6Z��pq-^fm��=!
���PЋ����-U.<���b�f �+A=�R0&n��k��*β�a�<��Ɯ�ÃX�;-{��*H�kȜ{V5~zZ����Q쪺�C�=�H*�������[+ET���ne����Xөl�z=m�ە����[9���,����9��ذ
~#��z�.N�Ӽb����ѿ]���,з<���4�⁐�@"���d� ���4*[�����Ne��=*8;���3��
[K�u%�1�c���V�M��r��z��Xq>��\��rG$�܁?����R;9����,�ʄ��SaԽ�3,G#++juQa�&nZU��L<"���W�h)b�3����@o���Bhp���>p�m��FްU�?nckS~�3C�HKeݥ�5�5Vw�_�2�y-���Z�f�Ir���x�]�b ��Ρ`%P7���/t�� �u,���Qc+cۀ���.w�������>-��hO��4��&N,�0n��0}�����.[����_OZ��+h}�c�b;�c<��ėf�6�S,5f
 <�~�ɄE�V#��~�Y�U����~�p�e���y0�JxE�u+�VX"g���>���(gK$}�l�RI)�"���vN�u`'M�U;�@�ű�wѮ��]��b�J��Ѫ5#�� Ԯ�G�gD�+c/q++����euDŶ��)e"> �F"���y�du7@Ї�ba�n����#o����j-�m�^�����+�-�����	��z��#�9Dl�W�U`g�8Ч}��yM?���!p���t6;͍y�_z�e�c|���6��Rb-�?'";WZe�aͧ��D�Ŗ1kE�1�h��̛�3q�h=�?��p�1�1飮���'�]��e�U�|
�&st-��|'�h���"9�}d�W�Y8��^>H�c=�`$Q��	.�q��m�_peg�S���nu��)�������L�_�t��O���BY�fr�6��CE�x�k��T�&	z}a�j��^Iᦟj���p��ksj|APCq�o�䙣��#��ܣ���q�'fߔI\e%Vc�
p烴�1�qM��z�UČ��>J��h%�+io���	��rf�V��z&�u�¢i�r��{+a�	4�S�՚�r=Q>��HUcĠ[�XAX������.�m�,�i=�g��d��sKn�y7K�6u��CJ�I~��|�]&a���h��o��5���|T�����t���F�=v�Z�R�;����T(�H����Ƹ�����qu;���Zꊅkg�	��as���Iv.��Կ/�~)�����w'4Yyc�J�EVnu�Oʚ7Az9.q���"q�����rS�i�(Z��]<�1]��g�fe��]��qu�����۶����ku����y(���=��H���(�Wc�F��f�+�
PZA�4L�+���^� ���/^H5���q؋9��+�S��5~�o˟�z 
� װn���߲��\5O�@qs�b��@�E�Q���2�]^�*�-Z���߼Sa]߅�+D8�ȕ�@��a��/s��B��>�f{��-7{K�/�J�����ޢg'����^$�>�6���� ��j�<� L޹��w�����Ɍ#DGz&6Gf�6�}��i�}��|ຆ㼴��FP��zDē|�"˫6�dt`����F�I����A>���@�ҔC�.�?���n�IX�{�r
\�8_
�������p�� R%`�����u��:��)V&���;�����h�Wٟ���8�-�s�\�i����s�Y�^��Y��'}�;��h�����HjQ/8��#���WĪ���*�	��3+\��>\�k���Da����������bߕ��g�$Q��~��r;$�Y.e|���D]��= <y��y��������6"��{�4<"��`�¯�K��A�!�Qc�zB������o�,CE���Z+ܑۆz�	y�9�8���v6	�����-|�N���07��x
�#�V��i+��Z+��"�~��R�{�+~��c;���B���w�}�����~UI��l>�3���s�2�'���+�u�}%S�=�I���u)3�������k��>�&@�\��`��I�A���@p�Ip��@p$�3	6���3��='y�9ϭ�[����z����z�޽����U��G[#��"5A�3_�2Cw�����MT���E�{f¿ќG�sOK�^'�	�Zr�#�-x��CG�
T����:|�h'2A�kR�-ÜZSm���� �� �AS(�8�E��Ӧ�:+V��]T1����\��M,/]�NN�/�{e�����ab�bd������bi�ξ~�h���"����H��$�G��צv�;d䟛���W�v�/�&�`�!/M��YoGM3�1�z�@|A�\���}���8�lX���䊺��/�Tu��2�����D�*O�TB�卿`y�	{�� >zН��^>�^y�G�z��v�ڑ���Ϣ�J�V V:���+���S
	�Q�>�����?89kKp��D� �'+Z[Ϛ���R ���:�H���EPDd���D-�֘T@�j�>���g"���W֐���R �n?$H�{~�Ɔ�Dq�/�(���������W��*	��m����|�o1=�~u��@��z��,�\�8 �ҹ��Y,�[���ڱ$!Q@`[�0��_:u
��[��:u齗�l8��J{*{}D�S�>���J#��i�s�h����P`��`[��[��y~t���tϬr�T��ע	�6��<cY}H!�[��jYps��%�4#�G5�f+es���Y�X��ӥ�Mak�����]��ba^�<=�Hߌ��3�Ej�n�V��OG��5Q�O���>\r�i|wZ��c>០���Uc�2��N��p`J�=���ٷd�8!�Sw�����7"b����Cآ���w�/)�`�����O߂A�w\O������XJ[$^3-u�g��|���p�����-D�Q��w���Nyns�TĐ^�G,�c��6�R�qg*\���o��<�*e�c�<�Κ�C�7�O-C_�o�X����3 �*� q�={��7`�\�ϳ�҉B��RKm�����$�SՓ xH[*��>3i�#�j�fbx_��OA;l�v�bV��N&�
XH*XG�%f�w\O|����e5��u���.�0<��C�~0$�h�#[kY��΍h��z��C��~_��h����`�2ae�`���VI��1l�+��H\1 9��&p���ǕF֨�eS�V�y��p�I�x�]󿅿.돡��y���VOm������n+�l|4�{�bE#�3^C3��n���Q�=XE#OEQlDF���K�l�Z2�1mg��s'�����@�uv�ƽ��ep��9�j+gs������G��U����N����&rpn"?)��7<Z��x_�f5tQ�UZx��ǜ+��Vh�������(�Ҏ� ¤ +W�@�e"�u<o��|$>�:K��>�U��?��DzE�OS���8W�n����|M{H(t��|?<�y�����n��
�\!#�O-�	��Y��e�;  ��f�<�ʀ>�C̗�����̡����C�y5[�U�~�#�R��Ǉ��tUN�ߙ)p��8�9����蛺頲��
��o(���%�}G���v�P�t��c;ف��W�7���#�5^D.�W�ݵ��mp�]<�-��H�U�t��ŵX]id6�'C�]ޭ�?m��$�j����e����d��CFY ��x��0:C�}�|�WWIL���E��$�,^3��]`��M=�V1e��)��(��:n q'[��C[�e{.�:�-`�N�Q��-M�gJA��Y�A�$~�@��k���AL}�F��q1�:���ju�2-'����C$�T��7�A�S`��dP�]��2O��񢮱L��]�v��
��c��*,5*�I`8.K��^���O�ئ��rI{q��)������V��͵�����oM�$�x
��.>Z���?}���gO;��^����aK�����
�ėz
���gXgY|���>Rǰ���v�`�FmR��z��q$s�@TyF)"��{���,�w�%`�op/JI�*c��dK_��������#n��+��wƔ#����` ̍��1\���G!��3��ܷ��"|��g�}�n��ܙ�� �p��(N�\ù%�b��_�d-|A�(_"T�Yf'���/p�͡fI������;� ������]����'��_3t�H��-Z!������$���Zi�SDM�~'���?$FC�"U�3�	�*�IQP�+��z��%QE���ܖs��̄e�.��>�;Ye�U���'?�w^�{a��N�H���en�.���Oǣ��F�fQn}�~XO��i��>��d"O��<�p~�p��yfI:J9�{_���z� }��w�}��S���G�7��)�.���U�G����ȅ�5���ߍ���R���
���󾈰��)�1{�(Y��:i��`b`��|H>LX��T��qJo��YJ�3�F %��{E�!����>���2B�.��ڒ��bUz~������P��@�����A�Wu��	�8#�xH�e��Y�-��$�n�(%݈�~x� �ѽf���wal��PR��ʠ�[��5_����$r;X;Q�'4�٘�4���$;zꑟ�X)�G�c�#�����b6)����5"A�m�C6nL������������،Jq��lHU��O��0-F�:d��C�a�4�	�7 RZ���b�De_��x�JըCZ�b�u�|��u��\���:4?�9��$�%\*�3�"3�Y�;�i�����ј!'{T��J�ޗ�*;QM�+~�h�R.���f]�~�åWD��H�N���o��9�%��>��ui�|��}ֿ�	 ���<~�_e���&6J͠'�?��������l�FJ
f~^���&Ge�����S��$�O�ܲ�A�Z�6��P<1?#	��BN�_��<݂\��ͤ����h�ٳM)t��pH)"��jp	����[N�����	�-��>��K����.[�1)D���GФ��2~%mO��Țl�&1ƔU��{�,��(�5ẽ|�?���l"��?PRo����g�� �uѧ����6��^T$Y���~�j����EW����2&��-ݫ,���1��E[�e	�ߚ����5��>`�RM���΍�O-sݗVNz����Y1�F�N����P�����32T?�u�)
5���)��}��ٟL�d��'�lg{L�ة����<�U��)(�Y�B�Xx*���Duy��d�'Ϩ�93��l��#�&9:{F��`YK��?�Y�ӮA�9&���v��)��]�2��X��4�b���Ld��~mK�UF	 �
d��:u�s�����}\� ��܄䈹Е�9�f|����;K��[db����?B.�b4�V\�e��LK�+<T�r�C���-f��	����J��1`��?x�S� N��HM���0� �}����w��U�f�L�	��x*o��q��sqTE�kI�S��Vٌ��8ci�����B3�>�+J�l9��_vB�C��%\�t�
}��>������b�{S�[��Q/ɝ��y�T�ٸ��'�����޼���� ��4+�;+d- /�Y'%w��]د�������7����p�4ϼ>'�MRDv^L�y�9F0c^�#\N[t�dO+��%�V��&�4ߺ���9��#�E���Q	�*RrbQ� ։,Ǔ5�p8;7zA�a��ˈ^XD!p��Z 2�l�K"�]%n^�U�e�����dk��A��!{��E	��b�y��f�&WG�٦M��ݎ7#K7�:r��h�oը�eY|)���.'h�R%ɬ�U�'�3P!\ڜ�UtNRw��������%�9� ��e�����lK�H���Uff3���p#z�"�*�2�����O�Á���t�����{$7V�#�B����3/�)]�?om�}W��(���/������)J�	��X@k��5A������㹾$��:�\�(lB���{����κ ,7���1|��ϱR|�����h���a���e}kk�p|}*���ҕTϵ�j����p���)	WK���u,ns?M�4A��@=g;���ŕ�w��waM�l������v,��x�W��������fF�T�`��ts����H�ܽ�)�����Q��f�W�B�.}�a�M=����?È�>�鲮���]�W�J�W���b;��4O�(�䥬ѯ����+a���[3�LQ}��8L���I�;1߾x|R�B�;�ܛʽng�ó��F��E[A����d�pO�0�pқ~T����(����93�X���z�t�,�=`�����LN:����m�,�)����g��y��_���g�舑�x|��;)�Wx��mB@�M�l�"�>��X�����w	�7�5��[�R3��b�|\s���l�f�\N�6��E��7]X��F�Ќ�慟�5���(X4kf��]p�L'm\���6��}�媔^���-oI_��_�?gPpkU��c٬����ϧ�l��V���l����j?�Λ"�ŹVư�gT�n}�d�R$D�����k����o��J0D�e��Z�2M2�K��군�d�Ji��y��mahmy�vY�a<��W���nl/��v��b������
���NQ�{�3�^����kψ�N��2�
�(ͱ�%�8WBv���_NT^NjU-�P�Mˣ�h�=�%9K.،[�ܛ���lzoS�ۆ1n����P��]��5�կ�s8F~�٫د,���nb�Bk�Y���NDr��a�x"]Xb�W�{�i��۾����X)�zh�'܉�ڭ�Q��=vi'�Awت�6�������@��T57d���8��W�0��8��r~=���i+\�1 �DEq4�E�f?�Db񠧿K���ɋ-n�![�D�i���a�)�K�"?l\�n^5P�N6�欠x;^4����n#�:��Lf��5���j�8S�-��ӡj�QK_�bl��p!��H$^)��-��3]�X�8���:������B�(��tt��Y[��ՙLT����� ��G���T|��B��qeH�N�]�jjr���ZջKSOkĸ�/�Ք�L�cpPJ\�G�OS�~o�q�_�Ah�8qސ���d��J��۹���P����ewr�S[_`�TR�v�Ƨ�C�tJ�Fw�rF(x�WԴ�6O������������F�f�YUc�q��W��Ϛ�����?�e�6U�􀈫�zO�_�fmW�j��`ٔ��[E��u{�qR�[�_�!��s+=�6Oϰؾ�3����s���XdA%Zc�%H�̍���u�1]0\,�����W��k\&П\B�kG1b�mE����~U/SFD@;��d��]�^|������ �0 �X�<^�����&��!l4�V}7��"5��G{=%e�8�%O������S�\&\�cVD�-K�u�/K�ڍ�������;
�Ti��ԓox�����d���������J!}�P������ү��9[%�=gyO�+I��5l^,(��HU���@.����,?���EF�q��摖�pM؝Cш�[�>�L7�u8�ܱ�)����ɕصOR?�Ꝭײ:v�ծ7	W�_�g!f�.��GCvQ��OX,@������R\.�X��j5`l�A��wO���wH�(�������Y���ORN'��z��]� ���X`��� ��?���W�-Z$1�.C���� q�IЪœ�����͢�<��K��e�F�M����i8=�Y���\��6lNW���� ��~:�'�d����n���->E��_�L�������I�ʇa���^	��{�ng�r�|�F~q	���9�'�L=�|�B�A�X�k7yX(7#����������,���3�F�}l�L���Z���S�ݹ.�<�]�\�&����f�:V�{��F~������ʫ}p��7����H�h�껑~y�{�?A��G\rp���ɯ��xj߇�e�-�=���m>�t�m��?����Ė4�����T���p�I�f��_��T��z��ٗ�߷N��5�����kE�RIÀ�PK�ζ��  ��  PK  o��U               word/media/image5.png̺eT\K������w�wo\��C�tp��44�!�;�Kp�ƽ��{���8�g��G�ct���U5k���z+\YQ
�чW�^��H���z���3����d.����+�o���+H>#7����8
Q�@,㞈6�[ۺ�Ud���U0w�����,9=o�HU�x���
�=��ac�����i\����`������Qb�7� '2⃔�F�Q��]Qd8�k���� _,��a�LTvx��r�Å`՚S
S�)U���2��f/a�<;�ߗzJT�T�v)pb?i�Lq�����*�ȋ�=5�C�p$aq\���_.�l���/��Q�vb\|�P���ْ��N[bL�� 6{G����ԎMa§`��zw�B�D(8�F�ۙl���̜���X��R�"~��U|C$9��U,zpi�gO9��ܕ]�:�.|)�!�1FNT�HZ�	�U�
S#�t�J�g���>����hT9�}�q|�N?D3�d*͈W���M,�!mJg�o�F�0�!�~ꔐ��oz�|���X
`cڬm-�M	n����~�l=��'���z�r�� X\�^����'K� ;K?���h�&�����x4-C�W��\�N����e�����;�bFT3�d�l�����d���jldd=;sL|=i]w��1�K�]�NǮ�T�����=�-��:��q{���ۼ�zå3�=�Muz3�Y�6J��2l�0:ߛ�u��F�əR�>J��k�V<��f�����9]��+h;�+i�R3�_���%�k�Ǿ��2�"�.�~l{7t}s}]�t7I���B��� ��TV:܈�㱜��z`Wa�M�W��hx�'\�' �r���5mZ���|�:�lAOJڸ ,�}H���?kơUle�8�C-{J�$�}%���$0�+���䋇S�yߜ<^�O�vQ��k��z���ׯc��������x41�p98!��&%16s�ŌG�i�� �өr݆
����a�`��U�:Ŗи^����O�;>:ڋ�C�&�/���չ�0agc뜙�<o��ۻ�a��_ZJ�3h��4�ٯ|�!�8k=�aЯ�Y��q�x >�J�m�OC�]T���q�VVi�y׆�b�B���ߔ�ZM�|Q!�{����y��¢Y��n�K4���t�ߐ���z��i�DH��Y��H�*�����c�Fs��G	F�h�.5<{7}���A�G�j�U�e�]��rM`B��?���HF�Z��n  -̽��e�بK���-����|�����֖!uP	����s��
��oVv(^=�����i���T9���RتZ�^�A����N%���1���~\M-���b���"���w��m~#u~���_G���1��f �F�J(%�aBβA]��K�	�D�ϝ�z�#pޤ�@��ﴲ��唉u�Uj?�r2��l�RMOT���?�|*vrGl�;N����=�G�(tl����ᚭ��g�d�X�E��A�հ��B)��$5 ���@�ꆂ��^{�X����8ň���|�6�J.�sН�T8'����y�Ȃ������SKq�Vֵ�
f)�>����-J�8�g��F��;C�f���DW%j�6��7��ψ���K>�A�cV�'����	�㛴��zl�R�\
s���q�Z������a%�n=#.�z��Z�/	�+���Gg�?��SI��z�'��C�rk��k?��ϽRs��c�������_�7��<�|.6���i$����g��"O�~g�Hg�ť�D��p�G�uO���3mL2�!��G���~�.79'�bv���H��k7������Vt��9#RĖE��,�Vy�ۥRB����1:Fk�>�Ub�l�H��n%Q=��UJ5P�T���ɓ��{��~p]| ��L"��.�\�Y�'�P��^	����>��|	�E����{~�����1]��clD��s�Z?$!ZJ���@�u�[c�ui�X�l�=�"�3�����U|~*�']w��*�ނ�k+2q"�|��6����C��9�h_$��=p��hv�\��V�<ZbC���q�\���GB���m�zW�@�޵��Ż�����w� �@���(�<�!,�S���9��&��kt
%�Rf�uL��#'�`� ��t�Ǳ�YD����r���oc+h�?t�V�lt^�Xϭn���˖��d/��*���φ�Q�漣��l�܂�-�I��R���C�Ge�4{+Gm��[��Ͻ?�{v�;���p�ʅ�od�>Bq�c:���ȸ�ӄ�u� �ڶC�݉�C'ډ�F�l���J�=j:`(�gm��r���m��i��(,�8[����ZUL�g�w|�N�\�sp__g��;�YG�� O�]<��[�������v(+X���E������?Ƶ�z
<�+���S��Ļ҈ԋ=`��/ٯ�yv�ɨ(0��Vd���K;�� n�RʗU����i��91 ���eKrVw�����.6:�*ȖFZ��L3#���3�Eb�y:��G�����L	m_V�E���I�v�S�^���m��S���6��󸮦�Sa[��D��>�cӇ�����|�)��O����\5���+9�����[���7ς��tW��3q���ź9�꧿!9�%���;q�����o�ȺB�~jd$P��"V}�<����������o�i7؈ ��w�=�Ar�Lwg2�_@5�ܦ�n�Iͻ39��H�üp|jx�y!p�y��Y��b� ���P�G��bҼ܈�z�<o��R�у�����x%�x,�]�e���������Q��kC�%?�pdAhb�p��XG���_=���d!ةD�%=4�����'Ώ�vP��C�p��O��4p��[��
��g)d���w�r���� ��t��Ng�D�˼ٰ@����q��TW:Z���q$=1{��)}�h-�PQ��U?0wb�I!��H+�p �mcw~�G���B%�s*�~%���I�d��#*�y�&o�.�K%�P�6�wfc`���$.���^AkG`���R�H�)=�f^��0b�sQ3��10���~��Q�ۻ6&���vu�q�
0�rby���D6̺���ӟY�ܳ��u�9"�OtP|~[�e=��%S=��ޝ}K`�]b�g��������9�<�|��������O �e��V'��H�C�[dj
>H�=��m��Co�O{���pT����-�q�G�T0�����+�qK7rgOI��+Y�g�K�����d=C�����$KM9-��F�w࡯𱄴��R?�Ӽi=�3����<2x�Nе*+~�י���|��FO��I�2 ]��9?��������r-(`�%���S�;q�c�2�{���ft3���XoP�~#A�XV/@舊�~V�`��+s-G���[�����*j�Ցb%���@��U����F�\�XZ"�e_����nЭ��A��ubN3BgU6� %BeLr�<K8UnyV��	:;D82�q����<Z��yw��[&T1��J�.z��8*-�&�·,���JdcuG��VsE�2"�t���R��W���,�����Dj�֋��n�.� �2o���&ڕH�I��p�E)z<j	�Ο�&Pٯ�B����N��LGm*i}�oO�ѷ�~\O:�[�x�1n��5���䁾��k�5Mq��Hհ�	K͝�9�(��̂r��5`�p���e��&{��>T:�'�Z����K]���2��;��{<_e��� �m���#�27���%E��+�)�-~���Y�'�t}C�{���[�,3����1�#�7���*ifs�q��0�]xf��0�B֟��It�R��=��i/`X�l�ɖ
�['=G�QVʫחpo���Xb�%x�ԜȌ^�xh�UP����M����Ά�@��p�Xf��=-����\�c��eǤ�7�&���å�a�!�"���²�4�*϶C�N�º��^��&�@�����E�L~Ǥ�;�?���ù���G�B8�r���Nd�	B�� q����'���gR��l�eoc�3���x4��g��E�Ċ,k�4��b�΅ֺ (�C(��O'�����}4�.u��ߴb�U{'i�OKc{��������D��E[r������r�0�LEFux�v�%&��!E@�&��f�wn�>���t���\ޤ�E�I@��y�KTb���Ǿ6�����+�N-���b�Kǝ؆â�Ą�S.:1'vFR�:�(�'��z��J�;c��\cy��;�dc-.v]�:��w��^�f��G�U��D��17g;�o�@_*�t�*s׻u�4�@�a(�檗>)V�P1��J���)���N�y�"����*c�@�W��bi7N��֪8ԝ��G�U�ξp�q��0p0���*���-�-ݬ�"�՞�g��x0�f�����f� vq�̎����C���T���{�Ƕh	�� {(��QU�jb���I��{8�J݉C��s�����Qt�=_lN��՞�}��Ns��`��x��0��ޫ1����Q����{^�_�{�fҕ���^*J���'��itn��#������v^-#U������^2�F�~fQ8�M���[/�u���ʌbR��3~�qӰ?���\9[���E���튍��oB 7�SI�\,�_����$B�q��eGR5I��e�l{Kc2����8�|g5[Im�Ģ�s[��QE &nZW��i�n����?������F"���c��w����3i?�"t��V�5��n���w�E�5�Q��l���w~�������-������;��PG�<��N���u;�_c��P�w�v�r����$��u����91�dsw���!gN�ſY�����U�E��%�5�һ��Y����M{�x!-�|i:��z��Қ{C��pMB�^����)��L���-4м�k��)��4\�ǿ8dtQ������3�����a�@�<�8LCm��?����9l={��9ײ֏��hW7��Iŵ6��3.�u�d�d?�U��x:�Qf$=W/_����<^��5� �yZ�m�y+�\��F����3�`G i����Y�זg!��sb��0u�Tb��G?�4�$h�$��5 ��?���):��Q�Z؈������L�n�1�}e�N�y�r��2>�|���'�����瞧#�&r�������^cV�pӇD��1�ON��C9�;��&�����wE1���Pr֣}}��'usS���H�Nz	n���;#���ڏ�`vx>Wa�Elz���l�`��ozR��n��%+P�E��~��d�%O���U��%9s�lsqn���ޑ��#=�-6ZYAy3gF}���d+��P	_�K���5y(5���OUf��Ė���.-o���εZ�xJ�d�q�O"���}V�/����:0�P�ͩ�bn^���r���q�R.r߷��s��͖}�P����x�0.w��p�w�𗵰��4�l�*ԛq��,�L��qP�]�uH���µ!�Γ�d�M��'
%`��OV���j�����,�����d~��$���E^�<��45�y�BJf>�unBi�K�Z�R��O6_���]�hܟ���:S��O�'����yB	9n�2�i�qaמȗ�.Q��e��G�&δ�,"f�������e*��/��rQ�v�ptM1�z�M��H
��OG�}E��M�<�;�BG^�RLW��'�bˎ�8P*mm�=�$,JtϹ��p�{���E� �f�o<�h����A,kC�s�r�,K� ���� �"�_��(2\�Z�!� �V�D��<�H��q]Tv��6����o�+���O�˜�Ճ�(?��%Ɔ�"��h@Wosǀٯ4��\>��y�#�@��b�D�?(|�+U��-��p��k}Q@�9ۣ�8��m[�L�
a����A��Pr�\�f:-����>��f�y�J}�Si[M��W��o�/��5�yB�<ZӶۄ<��wA,�\
d�'PɂH2����<�$<`E�}+y�:߶(�P�x����mU2[�h���3��:�^�n�L�J�;���M١��K>���@4�[bGe�*��zjZp��#�%oH�9J�Ŵ�_���]��}�~F>��hN����R���`u�Uw�����,t����$Q�9Jl�`���/m	�e����G�?;�B�w6(S��A��[6ys�J��*���v0�$�7<ށu�ߝovxS�J��U��i>�.�� ��%�𶖓�ڑ/��F�|,�&N�2�u��g&�zݠ� ���3-�KX�Jkq
ub|�{S4����[8��r�8*�{�Q��������1�Ҙq�y.��_����g�~�r�g{���+jD+�T,����� ~�����mF��2�F�����!��e�#�a���j�� b^�:n��t�)�"q��0�M�j>�q���x(/<������X� { /�
�'��>ߑQ���O"}t���0���!mQ޺\�?Wp���PL�N�a�f���b\-�V>���-����Yx[�Y������t���,k&M���]�]\0k����${pkw�L����#���͉[�K���L5*�G��f��s�����
��t:��e��(w�f0�&�Q|�����p=�����ǝ-�i�{P����6�.ր����z��8��9$����Yj����T� ���<��*&w�כJK�\p�ï��'W��v
��K(�Q!FK՝�z0���f��oN�Q�H��t�iqK@VB�
�ӒfaKK�p��OZ�;p:?s��������e�D�H�>g&�$Ζmwb�P�ׄ�b�U�Viĭ-n�D��K���q��37F��t���B%��4�߱MP&9�e�t�4HiS��ӦvĔ��J4�1�~��Ǚ[����mN�1V�W�B�g�m�akj��|�ֲ�-�s�9��-Yx`$}�V"v�L��$�����pL	=��'�m*9S���ׯ��Is�b���j������8D��;������v�ۻ�L/�D�`y2�0����d��S�X���i�Z��^��4�{��8���7��y�a�iUn�B�K�_D��f�ܜAR�V��n��)�
k��1�-2���
�_8�jAdW5���2^K��E+^{�ۏd4��/��Rɭ�
-�,g�+B0x^��߄�\M ��4t¶F|C�Y6�c�#�{�6z 7J����[�q`m�R��;�ǪN�|~ ����cIP+,u�䞜�������&����HW�_�l��;r�Q�v8�c�L�R��Wu�E�cE�&u�g��"c�²���pmf���W��c�|�[n�px��F�_K�%8����檮9JpD�S�2Spk�ᙑb�.����1P_͏f�z%i�aE�s/�r�w�#��OP^��Ĵ����������5�a��^���`pV�fb��@���L�ze��\F���HJN=�e����$)Qa���L�d3�����3H{�`�D+��[�?�r:_���˨_(� AzA3H����rK�{�mD.<��VXޖ�\�G�sӱ�)-~\wg`ߒBw :�|Ai��N�SC��=�#���U�gM��-�i���/�Vb���,Jdw�4A4�/)�E��9���������LsT���8e�
����H��ԅu�$�/m�:E�n��db��$��7D��s̷62����r`@s��xVO���ﯤR�F{���s�
H\sv�e���[3�߆�>(��G��Ϟ��rK�$oBg������q}�h&��-�uR������|!�ͣ���WWT��2�{1���`%S��Vo�o��Y��!a1����T%BE��)6�^h���9}h�|�8�Z���h�XL���Rēɪ��$���cӟ{�J-'F��^�\l�og��Ia�;4�Ɏ���=#�v�f��AC0<�g�:�xJ�چ��ޅJ\��ՠ֠�-yS�AB.��X�=�{���`k/�ro�R�'uS��l�㍘�16�	�n�Ebs��*�'?w�ȭ�3z6�izQ�}���y}�_adI��%�c �&�I*�&0�:�����*�>Ư�ƢCH�4E��<���١�N~p���.��9I�����ϣ�DH��C���������;�:2����~�b�(
��4�T�O�鑒A�N[�AöM����ȇy�:�^@(}9G6�6�>K��_t��S���#���Go|G�L�O>|�!��r�&"Z�|����b�-�*1\�G��4���I����m�as]|E�H�`J�eYY�;d��lĀ4������9�/�Sw�r�W[���<:l]��8{�}|t�t�R�ԩ�'�G�n}J�I4���\�#���ߚa�A�ɞG�>M|QW��67RX�������<X������cvX���@�T��4x�(R����::�#�N>dh�p�TX�#�����^�ƎX����3���)Kv@���$`���C+H��6O�6t��e8�������V�>����,�.�|�sw�� �����~�v�\#!�I�V�a׽{zT�NmQ��W6W:�ђ䷱�H�G�R����������P�Y���|���7lF�F��-�8�����揝�׌�;D�g�Y������_� L^��΂��e�j���݁Ƌ&[�W+7���^��S��d�[��~2�o]��I�@7�wǞ^���ASK�X�d�H�RV��<�7ݲ�~�!�t���=�"դYE���]WJ�Q��y�2p¾7s�tWqպN��3�i6�X�r��3�Sa�}[�����yJ�Y��,G����6o�T�14����k��>�К*���#���@���}�T{}�Χ��u�M��o45k!�� A�WOx/ds{�6Hw�Ȣ�6r���3�^��=_��]c����J�x"�� ��ǎΑq�>T��昝il6�Z����`!����>�f҄+�@3]�}fx�lB�ގQ�w�w���4��5/?�%V���@ng�2$�S��䡤d��t	t��A����+�9Z��Z�j���\v��ͯGR�>����E�D��1:�7����/�_g"�=5�%���}������$�w�"M8Frt�%���d'��HLUb\'�t*�K�����w�L����*w$Lr��!?���0�@��頓��P�(Z,W���&����tP\,�a�d��a��YM`@�A������*2S!S7~0Y�d����t����0q�N5�r:��\�����<��?�=:T��s�Gԍ��o���:��[Zcr�E�RPZ�ڭ����1�|��gw;LIpN��i����'����]F5d�I���K�D(����p98n{��jG��]� y��b%I�������l�h�i���!���1l��眠��\\s	�_B����f~��9l	���}��l���>Pg�:\�m�R��AF��C�U �c�W������ur�^��c�DI�4�%���}A��}��bl̽n�H�{4a���i
]P�O�����z��� �#��+���f��" |QpD��UL+�S�i^~
�>H��e�]�J�Gm���T_\�ŕ��`(�C������^ڕJ����a�܆�P_,|nF����y��1Y�?��s��[�����.3nH7͞���u��k�te��ыWJ����˲���\m����ɟP +����m�s��g������-VL��ʞ1�1��C�4�']6Y��B[O�M����+���?�9/UN��q�ޱz�c}���s h�Y�K��6ze��W�������q���ڊM�?(���zJӝ�ָ�}|-��E�S�5^�0���il��/�[q�N	�m�f��d�x�=QLrP7�hM��A[�f��~�Zgv�9�O�N1"�.'�M��FKH���E����Q�� �S+��;����Q�l��iD7�Yd�G�2��M�V_5�E��ؿGe$uQ)�&1� ;[�z~s=c��X���*�o/���F�%���O���J%��g߹ʿʧ�ݫ�te�\�89|��u�]��tv�+��8Wi'.[�$�=����;w�t��� Ǳ�����ܟ�k��x��Z�HSNL��v;���jt�gT��fz�w[Vg�S�)�f��m:�h�9V���Wn�����V���MaoA�[
K���c���h�%�!����}����|��b���g�7\�����f��/	Zu�w���O=��v��Rf����Ho��u��kv����"9����Ci�Q)����?��(����}�^���7n��wx�3�+�V�06`m��� �_$�A��Y=�+쿫�M�����A�.��˪-A��	� �;���w�@�AeX�E|��xgtm}#��!�v��������,U��}�`deC;S�?�<�$g<'��xJ�4]���Om���T�ǵ��l0DV��:!�ѡ�/l��ubt�0M���Bq��u�E6���v���Z���Mw� �,P@uQ2iq�-��Ų����E���,���O��Xj�:��
�R�����_��S4��w�(�� �f�М�����nU�����i��W�c��2Z�]�^��7�n���e�B\O9c���~Ϩ�l-�)��[
���tIV���"�����`�mµ#߹�]H��n�+TJ��,�Toj�׀S�r��f��u�[l�e»&c�鲞�Ij��������w鹹�Ƈ��3�V�펲����>�D����SM2����w��x��y�ҸtB]I��{���ނ�8���N�R�)��`��[uJ�<��[G��NO�4�[�k�%	��2ƺ����u�';~q�V�ͳ�\!)�K��zb+�O[�8`>[�%����:X]\
�
��!*��"O~���5g��ݫ�	%x�)-
�|��XH��y_tj��H�w�"�͢�|y�'b���1u�{�����A��ͯ	uLr�mѹ�]�S�w�2����ؽ�F��[�I�!-��]18�m;��F�&��Z���Dl����Q�_����YI��:�n����������]�" �~:ϵ�L�j�ȋ�㸦�F$��2��Ҹ�O'����wlm���^P׋�؛����̐�&tV -�ɍ��.32"��zY��p�Rd���z�n~I=�!��#�O����c��:�=JM�� ~?i�c*����8j�J�Vз�	���َ���몸����R���A��������}��@	G`�q��ؔpQ���;p���*��:񯰊�@m~�F����������n�K���q��G�l+~��_�-�K�--Yx�#�3�������wA����ݡ�|��aKocH�&�{	��|m
-�4�'�*:���`1jr�����+�~Ak���`3�o(��t~֣|DҟR�N����p� 5��iI�y5���=�>���H*ٲ=߸K�Fd�/�i�)<;�b����`qf�q[7���]AO�6��9�M5:������tipϚ��2_�ii��f5����l�['��j3TV�Q��>?{$��� j�_�N�𽭶��T�>��yJ�[���,м�����^a�[G������Z��O[�z~*s�1�7UGn�ÛsK�%HO��
����1�$ڱ(�������U{���]V��o�s��e���%E<�j[��Q��9)8ٱ���lŁI<����дs��n	�0��(��?��:���|	E�[5s�����i�h���a�N���d�*> k�1�Ȃ�������Qb~!²�S}�	��~��-X��IfO�g��]ߚQwڀe<z��䅊��M��̗X*���㎓3}/0k���EZ��o��1����<�.4��'o{\��(ٰ�W� �%��>�T�S�Iri�H����fl�J:{����td���y�-z4�1s��w��w��\I �x!��n��	"`�:}�_�.L"����Q�\BS$�
K��FwOs��%Ϊ��g�)�H���R�$)Xs��P�k�^�w�
n��pǆJ�ƅ���M۝�a�=���E$4p�����15?b/���?�۴�*�i>/�����������)������U�?ꁊ������
%��ڮ� �k�UZ�f�����#����!�w��Ş�\,"��8UE��r�멲fǜ�C%���wTt�_s�9R@�f�)ȁ����;2��%<rUU��	,��Vap���Ġ���8�m��r�M�K���dt��7��Q�k�y2�l���id7{&�{RS���⯻��ƌQ��5tĘ��݉A;�����+k4)3	�=��}�{��i��F��c[���7�I�"l�(�}�T��~�nw�8��*�U�~��{���#���&|���Nl��>0y���C �&�_�a��*�_���f��C��6]��7�.k<h�Y�}h�}+/�VOKha��$���,���w��u�$�e���A4�'[�g���\�4-��rRu%Hi�d�$�GcnM�����L�\U*��vpE[���������H,���\�lo�敡s�������F�?C�Y�'�lE�m���0���A��6���5�܌�yGO�M�e�1�VI���X��
��l7�8V7W:�u��gF�&�ڏ�	�`���>4^�������r��Yj�M�G!_޷5v8�}(=�Y&u	��՜Z����:yQ��b<����7��Ʃ� ����z.k�SEQ�����W�$?�M^'��)'(�����wx�nX;�р�X6Ţ�K�ƤU6��2��M)~<��U�x��x�F� K݃�z�x۠hp�t���W.��Ӻ�ޙ��R�&"V/���O�%QC9���{��.�}�ֻ��&��K���6�J���:}�3�U��6�1N�q+�|�6�R����N�Ry�����CĻ�]V���?!���ѽt��-E���#�o|	���ΨZEh�joo/�9�t�Y_�T��F���np=�����)}�-��z���?��A�^��u���gu	��f7�@��3�R$tP��f~	�bc ��� ��g,kN���q-(�������ى�؍��V�Z�.��s��9�#�^N	ߎ���:��,W+��{[#-���̭,o���=�30���g�n�v�$�k�����p D���W�8��3M��P6���&�
{_4�=�Cѐ=B�UH5�rN�kz���&z����DWL��T�n���}��/��)T��a�V�/F����RoN��+ �pcx��&��q�x�k-��9�F0��I`(��ߜ���b�ToF�څ�3��X��6�i�<d=1<�o⢨�����L��op���
�n�1�R7e�}	!��x��k�?*=���S�o�L�ף=>��-=m�uK����R&q=�~Ch���/�Y^��*-�mɋ�R��[q��P9�~󢏻�1Z-���撫 ���_����я�w�˽O�E�d�,`2���XB>g�\N�e�X׍�RV
����Y��' р�l9*��ނ�o����'�[���Z�����U����HH5�ٜ������5�E��r�w�G��Y��1�u˖�z.'($��P��p�y:��3�y���>��ZH���@�#9_�U��Mt����gSL�
Mg�@���^��wmҚK}0�; ���$�+�d�)��ӯ`�mm�$�E�}Y8��4Rұ�}�5�z�[�`1u��ſ���F-�|y­.���&���9��e��V�FJ�ܓp�vI'm�@n�{9h߽�n�vAdk =�AwG����7J)cp��\���6(� �v;�hk���Z��(����_I������c/��;j؉@{^�{��E�d���E��y��� �ҏo\��bb�f�d�(���bU?}yΗ�6���;8s6�� ��<�=~[�*Oi-g0V	�B�d��~я�����Sm��˄��S���%�Y�}��=f¢��$|qx�˫�(2Ջ��L(�<x���xOѳS��A�Z��sS��?�o	d�e[���s����͆�M�e�˫���(��E�ZIQ@�t�n��9�H�������Pq���+�8z kI���OֽVo�-KeKz?P�CeӔ�yG����t��KlvTgQN�{W[�j���`���u<���D&&�<ܚ��`�? �>i��Z�䓭#}��^�ߗ��L���<�����<W{��`UT��i�[=�5����7�ڤk�[��0ם�f�L��̍* �H;`�9?���/�*���c�}|�aXm�!������X�Jc�#N�~d�S3Y�����e@M���:w���Ȣ-'aG�����rwY��%7�H?��w/7_���<<�р�w1d�%~��e��)ϴ������.�~(rZ�����}!Y�Ơ�Ty�5k������?�-+�/{|3z\����N7�ZS2^L�`�8�����E��q�V�T�a�%��Nʑ��^��΄*I]1��v������r��Ì"��\o4$M-�d�u����4Ɣ��T���+���?�Ez���X��{[��b��[u?!t5�W�/��ۊ�H2�.^7�֪��F�cq��G��9]�LVNȧ�%.*ÖB�t���?�Gz�jxl~�x�B|c%RR�A�UE��m�U۝�i��i�;&)�7�$��c˓�-��]�N��o�ޞ�}��I*�����#`fW�j�r��9?@3���V��Š补����N�(C5�,�%����We"����[��cB������F������H9�u���?�G*Rc�"�2'a@�ay	򸢭Lw�>F�LuAϷ��t�4��oTb���{��g�u*��JkU�ע
�ۭ�(ADM�U;g�����s���I�L�C%��mB�|����l�V�6�A�o���MW��4�Me��j��\��G�wg��"Tҝj�̆/�w�;����62C����]��ډ�Dy`����7�zw�O�D�L�vz+�u��Ҙ6��p��2W�w�J��ql?%��,@{���d|��������t"��/h��i
�%7���ʢ��Vu?`�:�
�!�%ڕՐ�Hw�7?�����T���+&�a�3�"������`��O�80\ǆ/�h6�m:gʯ��#��f�f�"|X�����L<ǵ�t͎���lSUd�ʆ8�et�TT�o��F���`�b�C��r�g@<^�t������gV��|���'��и�&�S�J9Nй�K� .��4L
D�J���b�{��x���{�_س5y��cO������⑐d.R#T�y(�y�'jVV�\}�Jw����"�~�������tut�����f�����:�d��y�h	4��._`rq�+�kT#����[=�ɰ���.�=���N|���ۤ�p#5'���R�,C��[�"{do���QM��K^�'RN��B�7�b��*y�
�b����S!���uߒ��,2�]e�5���7�*;��eE�h�}s��i|"�P$�&T��Dc����S��K@֜	�O�c�hO'�O_;�Ln�I�1��#XJL!����B��h�㩰6�9fTx�|��>�B\'IV����hؾtT2n��<�qtTh�`)�����6��T��1f4M�f��+Jlsi��N��t\�	�A���i�'z3���U�X���__�?�Z�jď�����̦��\0kh����խ�)���e:��Q�c�H�Պ��ĕ~֠�I������Y#U<����%�c"�B5rc}F�^^���K����(�N"�uf����D8\x.�l^M�-|���֗:z��m�إ�
%����X��I�O�FeE�Pw$��-t�+��ǌ�Ka�I�Km�&����̏����pW�t��4�9�� (�3��~�'�
��(Es��S��_�[Ĥ�cQ��d�+5����i�:L×�����Y�s���L#6ጦ1W�ϓK����TZ.4k�~NFz�%�t�	:�M�8�B���F��\/j]���Z�GK��)���ڎ��F!r�?���ٙ������G-��Z�$ěs��n�Ɖ�$v��}|וK��ǟ�yw)R�^-5B<�,��?|?��R�S�S�lבqi=�B�_�M�P��L�̽�B���ս��s���'3V����K��<.�)�7,W�i:؆/3x1�+Ϻ����lf����z�}4���L��ɛ�g:DЭ�����V�^�[I[�&ZW�5��F��$���Ms'of���Q)���?���;��+��΃n�G�~�T!�-RY儞^��j{�ye����_]1pO��rfxFz�VEB�ħ
�"W�M���`����B�%G|��{�*f�y��p�7E{�@������j���*�H��?/܎t�'��|GB�X����^�?ܸ�^�fc1�������J���-)�$r��'6��cQl0]�F�VW�G5_��v��R�))*̀t�&�����AJp���a )�n�n�.��z��~�ϣ�;���7?��s�s�s]�\�Z��p�gM�a�����})�=�����&�ǻ�)x� ����&A�F]&�6[�]����t-��jJ�+;�;�n�
�^�Ж"/�m ����`��{\ �/� �ԉo�xa#�Dqc1�d���*O"B	C0�*�)�-�Z"ȣ�1�y���N�,�0����]�5w�	�MM��,�ڕdT W��j�9&�*J£IQ��7� pϘ�~}O:�{Ĭ�<���3-��3U��z]�aM��01�3��mZ,���������zշ�zB^4��� �Ƞ�pM���r�������!�S���� S����z��H��VrM3����)��|q`�ܾŻ��|I/�i$�+�([̣�K�(O�a'���\&����X����9(��DƇI���9�.�����~n�L�+fC�D���`=�휟��L��Tً5j1��7>a|Y�c���?YF�dJ�}�[T���N�O�;�����h���.�bZ
�_�7�tV8�I�qaC�@b���Lw�IÁ7.j���n�PͤU�V�J��<�S�]��+�(�mvh?0�iO�VB娉�9������_m$Ŝ�Y������UK�H�[	�m:"3��R[c�8m/@�/�����5Zx;r\p�#?��k)�x��}$\��ӗ�����]��JaěQ	#�F��l��Aw�����f��M��!�7�������|���+e.�j��x��aG���x�(��ת��v�ӈ��/�Y��n?�3ëBɍ����c�z�1�PK��&ON9B�A�����?#;�Kb���)��o���h��m�5ʰ����l�|�C��̢�<S�_��F��L%u�>�m!e��۪{,�[P�+��14K<~���bM(we����{�A��¶��@�]S��7x{��{�6s��F����f!%�CJ\�Ġ�5��*���+�Et�O�]d�?y���[�A����ʰM��6�}���XR�L\�Nv˳m���Fr��H�e�,�\��R����w��V^� ���d=�$^���$�w��B��n���"���U����7�)�ʀ��z��V�d��
s֧]*E��6w_�P�'J��X�100Hk,��b��(c{�^�g�s��*Q��5��@��������k�=�ś^���/�,�9u�"	3����<��5�L��_S�V�K!��5��
�t[L$_�Z�[�P�lu~N��tK|0�{f[@�#���@�dMSxW����@�A�A�G��\�4��-�K%�H�֬���(}����<���h�Y�����Ω9b��PH������\�g���-פ=��g {���p��g�؞��rUn� ����r�2
j{"�p>5���uWI�bU��}�
qV�1����8��Z֩df����	Ƌ�"/o}U|b��D4s����#ҵ��M$7���s��*�hӿ��L�wC�\J
�����_�q��_�$7vKiX����e��Ǉ{g5���`��K�+%Eє��� 9	J�M��o�\�#�����p Ӣ���.��K��z�Ӕ].{�Ӓ��/[r�T�ׯF�ғ����sVcv�5��(H;��j��IMj{���'�FO����ڮ����3�#n��=�Z��sW/�ᮢڣ��Y{�Bҁ�GUkc�͙m�n4�{��h,U���g���%h���>L٪OIB��9;���,�U'�L�UrZ�q�Y*�OF,�0��d1w�����}�Jr�gYz�p�7��^B���R-�|Dz�h�%K����&֋��b�cV^����n���Oɝ\b�f)�E�M�������P{����N�p����QY�̀7������������-G_�ڢ�?n�bK,��R0��i�[)�<�:6�o<	1_����B~q�jչ3�[�r��mA�ҭ���WO��g��Tva箄��@�$c��ЭFg����a�9 ���o����ڬ:��׻����YڷI��Yb.�Q�=��7���n=v� (�S2�ɺk�;�C�d��p��Kh�`[��D���RC|��MG�8��!Od��F�2��O�[��́��෕b�J:��^d���b_�*gɧ��{��
>���:>+���Z�)�c�R��.1�U���;��m&�'37f#��'g��>�F/,~�K�T;4Z��0�"y򐺡^�g�V��҄/�/��+xg�N���`/�w,G󎉈� O6��V�7ę���olaٱF_>Tâ۝�'7�;9"rL���D�����9�s`��������͡�=�7!^������I��l�d�jzW����x�32 �|�؁<Ӫ0�
C�^Y�.:���p1!K�N��d|"������V���pw��OQ^�V�����+!J�����}��q@�$����᥸��ys�0p�ӂHM�f����;��2X��Z��
\�X��W�v�Lo�aGi|H��R��F�\ۯ�"U����Y:PT�w��&" &4n�\aץ1=�Y�i`W�`n��jG�&��ue_���)!�~�~p��g�E�@	�;����j�����0z�xÉTuA�J��,��k �F�K_�o&b!�ȋ��#��&���Ί���*�<:߲�M����9|�kʦ&���ѩJ&���_L֞����O#|�ת�ߥ����;y&-�|��7����T��P��NSK�f�P�iT~�k=B�����
����#�l�B��v"Nc
94>�C[�x�TG�n�k�D���v���F�r��_[��PZ߳�J}�A���sm�O�+��#�U0�U�������Q,��>79��|��ϝa�4C����f��T�dK�i�p3���S��d!�J3��1��Б6�Ց�LV�z�V�x/��CY�\9uNOk��_.�3	O��&~�!S܀u�P��1��:�k��~�H�ϡ��ұ��	��uϵd�������t#�V���feԞÛ�I�w�S�ܨ��<��"�tX��1p��Ж:�V��)�R�	��#���'k�%쾳��(~{��Ed�P�ہ@:�[�?<�?<9��H�t� -ګ\M�^��/�P�:���F�����1�����q~�<:�I_n.�P�(���e�;ў~��{��溺�x��|�p�:�f9c�X�P�O��ϱ>�=Ex�|� �J� ����V�6:���v>��֚�Sh����/�h��IJu	��JA=�W�`:�[MM�Ɋ2��4�B�O�G�C1���ZCj��Z�q}{�!�7�9^E�3w���7�EM
P�0�m����ǿ��\
c��j���bT��Z|�3�^C<�ÍCi�A��;��^��X|KINO1�!7ְ?�Ge�p�� �¯$��ě�,,f}��d_3C֦|�ȗ��vp��>k�6�8m�x��{v ��l�:����<�ːTI�-���JY���-Wz��s��N�Io����.�T1I:sd�+r *�rXu>G�@&"�d��#q�bt6/ʉ�х>��Im�Ҵ��*tX�у9���[����Z��ƌ����+R�Lejzր���󲴓)=�y�LC>� P�({�I��}:�ǟ����2��,�!�_�6		0!u������֘ny���-m�MY��?�����AƇB�N	a��"��1��DBI��%\s��_uY�(��&Z��=-U���|{+�+�n��2kGɡ�Ƒu;U�Tt��y���N��45�m�gp[�k����j�L)�N���ymE�h�;ս�9��A���P�Q�*��}�.��^+��fӞ�d�#��}
���
H`c@m vm$!��OV�\v�͡�Q�F*;���	j�>iɴ�'}b�@�¼�~ۈ��t�3��S^A"��T���Swɑ�|�o��oL>w9$�?=|3�f��yxh��p=u�n�Q\ՈZ��ъ��7���GB�Z��U��N뉎9�_�+������:L���/�'1�jəv-��`��1�{��W�^�3r/��r�/K:`0�N�fI.�:������Kx`������D�<����T#�\ۥ��l}����~���q�o���@qw���9��H�/���etW�E��&�;��(�"�3����j��!��xr/<@x/��~9����}�έg����/�Ca�*��/�O[Vc�/��,�P���K�>�\2 ˠі4�z��d�����C��l�,�������?E���xSK5L���!Se5+#`� �gu�w�hȋY�G�`yk(�k����}��J5���ȟB�m֍N�9I��1�!
EKS3}��(t|����hLC��xe)e-۞��,���(�d��ݐ�Ȝ�ط�/��G�!���pL�N*S��Y�T`�w�t�:�I��4p	�𭫡�Ʌ�֩��ݓ�ET�Ɗ,9��O0�<��%���[ �Uz��>:󽾒��/�;����X��B�u�xW{�B��!@s�Z���w�7X��o���ߩ�cWw��*�`�9�[�i�F2)�'A�����o:�ϟ�|�#�v�]����ŧ�C�~lsQV�����C�힀nN7�P�����<{�Lf.��{cr`v�Qvo�P��ԫ�e&��ϒ��55&�Ƌ��)<(Q��qtB��Ra*���j���Zf԰�]�i��~����K?�/¿-!���:�6*�r�_�^�D=X��
7HP�A\�E�J���?e皀�]{��v�8�{p�]��Ӻi���6:�l��F���K�b�/�Y��@�k�̛��\�ҳ�3��^��Ǩ>��M'`�ՆJFR0�O0;V"�H�Z�;�s,��u�����92?c��̟������������=����vW��a�=��9�h�3��et�_ڻ)�O[t.v���$&�XP�ЙfnV�\$\����E,��k,�K[e;��zi\i��j�ZX���2�meH}���1�N�T��VrZ�a��0%p�o6�n����#D4����%Z�&L�����'d�m?��'etK90�f<LK�L���V���ՠ�3Z�x'�j,D�w8�F�3_+
�6�����I������_��#����P0��L"�_�U���&�n�Ii�Ș�m�����_�[���lS�R��
���Fh�str���b�y�IaQn�5 ��#r�:��e��-�P���g���!D�C_6���<{&���77
^�̻�t�<��S�2�("pD��_4~��P��3��
�sRg��X���pg�����2D�6�
,~n��[|�])�?��I�q��d��� ��M�6JZ#��1z�d��4ȅBָ��9[ǋ<V�d�5�$�2�sF	�p}3���I�A��r3�.�7?ҩ����鯃m���며<���x�ȎG O~���)r���9�*-��|�`��䂛���'��۟̚	m'�tm��^|�NVz�P�S�UV#J4�˓�GV�y}�K��
r�w{��=z�/co�u�wT���ǯ�tG�&Y��;��S��H�.��-�WWH�3Ffܥ"e=�a�%�\�v$�Ə!R�\�!G��ٛz��K�D�Ѝ�Gd�#��W�����M��^�^��,�����V�?�,��q���C�D\�M��m�L����O�3}�����Z3f��Հ��d�9im�p�фb0�a^#����������>36�}8.ܓ�3o���j�&�(�>��P�{�9��f�B2'�/-q�w���c����q��'0zZ��"�r�뇳�Q#Q_��9/>�����>b#��W0��E��м) 0�'��� �f�T�������. ���@jŉ8?l%I]]ݻ���n���O�݀��g+|?iV��>P�%!k�D��0Pf��;�X�P����Ҥ>v姐�NJ����m�+Q�M��!l�1{����ߚ�4���?�@Zr�����C���[��X�.u�?�S͝�A�=Xb�#����3Ք9�\��~��Q�hl�8J/�J�˒�.?����~�������|v~^�s�6��~c�+l[���-yW6�ƍ$kz9(�����I;H>��,�-���1��ъS�S�B2c+g}�My���y�s��HFo��}gZ�m����G+��g��֕��6�~Vz�z6�(�~@ƌA������D����Jd7�|��J�2%[^��QE �2�����T`������7��L�-D---�AOF����=%�������f&�]���X4�/��t�fjA�Xu�)����8�FT$�1�]�?'�D��4��sl�ώ� �8���җ�5v��?;Zh��=,V�v5t�p�P)o�\D㨶`�����ռO�L���9�{��¬�M�i��5Z�����d�.�Z��,/�#�����
�7�c�rz����tI]�Zd7��G� �Qbr���!�']�ʲ�2l�SI����%�	^`���U��o��a1�|:Q����K�X��J�r0��2�9��>/a D}g')p����S��L�M�Z����7���ة���5	�$ń�M�/����$֘z��p��נ�;/����U�7�w��}xηBp�|}N~%��4ޱ���bR�fA>����JD�CL0=��k�v�]Lf��:���1��#SĹ8>c/8�@���s�IB��4^����<22����!�Q)s���b�lՅ��"Kԓ>�O�'�{B9yAc��a�\
T�� �a�G�AF���0CS������s6-.3� �.t��V��m%O�+8�UŖ�ĤnVJ6�����M1�r�R��l&��$_�� �6,UMQcnE!�h�Rp_���9�NT�3y�!"��4#Yi&�.'��3����)�v� �#iG$��̖\���(+��S�)�z��M��=�!�#��<pJ��1��"��u�3�|>�������n����|��of��[#E	̔y��+sK%{7Q1uHaGtXso��'I*�y&�?e=��?#ُ�8+����1�G3?���g��!N�;�N�˾�����=�,q`<���ve�� X�v&�/=nF�M�<��/E_ʊ���02���P�Enqq�������a (��4洢iˣ���pK����^q�X- E�;�7�+�>#�y�Y~[�ߘS	1QN�����M��� ������m�Rpe���<Y1�ΰ8H�f �B�"}w.D2+�ڒ��������%+�>�࿰�g����:$�ӏ���iǱ����2!�ʒ�{�	�~űAc�1�^��,+c*5�Lq��V�^2^� V�Ic����E_��*/}z*۴i�9}N-+Ta�5���&�>�7�,9L�7�OG"㓳u�E!A��S͸�����<��巏5��������/J�T:���t�����7D*"D`.��39�*�h��7<6�YL� �r@O]~�V�טU�H�.K��NM��*��c������.�x��N����{˸�����B�dՐf�|�[���x�O����}iu�KR�՗v�W5��\RQ���ق���{ܥ�|a��@b$���[[���c(b���c��+X�K���E*�,�p�d��RB�Ƣe)5W_��yL�I~����n0��S��G�d&��"٢�k:��U����<�%d�1��D���a�'�����±�N�2�-X=/0e;.J�d�`�[���.�j�F�i������R�UAM\�2�ݥa��.�HC�A�ǉ��.��%z�9��:Į�f��,hW����5�J��1�RbC}-|�xo�d��|e����^�@i�bA]��PK��+�`  9i  PK  o��U               word/media/image6.png�{Pcݚ��
4����wC�7�ָ�[7��n��54���.!���7Ssgޝ�z�^�R����}��g���o%쇼$�'�O�����oJ��F������-�{���2m���U�=�|��,�A0��-��O��xKA?�������S�\ݼ<�Þ��=�����p���B5�\ ~�7�?{���Ü�8{v�N[�/��h��8ok�hL��p�-��Uv2��1M���I�~s�͋Cx`	�)_���P���f�u�sr�Yf.Wۈ�|� 0O�	d:��Tݝ��̿���A��s�t�V� Y'E��D��н��_�Z�`����_�����7�r����F��<�O�2�3A��
���r���18l}�X�G	>I����*�$LϚ) Lh�s�u��/cd6����]t�gS%��(�䈟���y���C �;	��}�م��8}z�P�+j|�\o�-��B�x�G��M����BO#:R[��\{�Zڷ��-Lr�)}�<��~

�Ȩ(��$Oo!���OC#���noQJ�'8m?Ɠu�;�ԗ�b
����}F�x/�
�-�g/:ik�K�8<=bo�g����"\w�d��8r�=8=�����nR�)�t���Bh����|z:!(��g��ƾO�7߻ЍRYǜ%=q�	<��MzM�'�UDBDD,����*X�}��5�r���
��Rd�Y8�+��}�(P'���f��ą���S::��vR��q�SCKS|/���@b��P�7G:�E�����[��헱� �<�M��cm�zF�rcMT�je�=�h�����$*�	��IX�Ǭ[|�#%4����WM7�{��g� ���L8KeOW-�@�!�4XF2)����\��(�
�m�N��8�LtJs��|)r�� <��by$}�dv��|+'��~�(
���;�Ƙ��J�E(�2��t�%�f}T6Yͬ���T�+�v�{��X)��u�짐i�KE�%\F�����y��������4F8-����G,��Z'P��k��LdԼ���=�������W�/B�`�QD��c���T[�O9���9��O�/�1���UL�{H6wOº�slU^
�)!.�]�.A70̲(o�E~��Q�~No����XŊ.�`y��&��$�k��C���g�>���.[$I�u�q��1�
�$��.�"�c����4�q$b�b��)���.�U����<�>Li7�+�&1is;vC ��VV�y7�B!�^9���~�F��瑩GH�Tذ�j>��_J|ay7�v�=qʽ\o���'�Lι&T�4�MfH���[xv���9�f�O��+Ytm��β��L#[&����֣d�t_���,s-�eSũA�,����/�4wt�j�&,���j���-^���ׇ�N��k(��0���դ߬�e���g�8�}0Eᳯ�H��֭�K!�d���io�����_�;ץ�����N�w)�k��n�$&_���9���"o����]U���z�����~J~���h�J[�ժdxwr�G	l�����%͈���\Eu�0�t)���L'�0�xt�] ��ĥ�ʐ(?�f��-W=c>�'�D�Z,�K5����h�8b�����*(M��ocu��Q��mս2��M4�i��&E6�$`+��V:�Nt���C�[�#��x��	�P��/����S�����'R!��Y��姌磢]7�^�|���~��E�]j�,���~�+�	չpH?Mޥ��h�ch�g�-k�T���QI��j��R�Χ���8���7��!��O�䑌�2F=��K�F��Q43��eCv;�9kd��Ԛ���c�$�ٯ��y�dBE���cz'#k���h%�������F��Û�GX�Ǚ���C9`��܏EG�>�@9D���QV5>�c��e�N�XV�3��C��F�9�Y�>�?�J5	��߳~���
�^���&�����E����4l5�l�2�A-��޻�\�BK�
�����A���-�)�����9ქ|0��-^�_�ӏ��?�\f7^�K^���4)i�
���Q8M�',\1	��`�?�2kh{F#0���]���Ng($���C��
P�f�J�;�H��c��L�G�ۊ�/W�1��J*�̻�\L?�k�Г!��b�2� f��ON��s�gI5����T���E���tMC4�Ē��K�|\�۵
�-@�?o��Y���[�����jK�8ݢ��.O>a�֨ƕ���4�PpޡO��K]�{3h��s��������$e��D��I��`�<��<�Yi�K����+2׫Te�މ��x�灋�l�>��$��Q�� ��"�$4�Q�D�ߠ묳b��+\l�>c�ʛ�*E2I�~~\M~�fN��rJ�
ZE��#N	�K�`4A�}���\(A� ^h�&>�(���Z�Ү���O(6���>�MoD����\�y�`�zf��z3",�z�$�m[���S�>K��ں��c��p*="�ކx�������]�bw��ID��H�[��t�u�'�:�j^�הL��]���:xf��N�ô�}�Y���Ga*�����fr��WD��,���O�M �c쳟�%�S���B��6��g����σ�w|S�@l�i=��|-�u�d��P��C�g@��Q�hƬ�Ly4���A�$�LZF2!�s���D��`��|PW�z�g�	�7�������ع��{(����D��WnG�o�%���<������Ovy�![�+���KU 1��E�(ow���:���Y륎~W�
XET���Qp�:�NrN�%dt)����QHG�ۅ$|�.��%&�`=M$���c��%ܜ�WL���@o<Fe�"�Mô
�C�N��i\B^J�]N����-���Croq�}��[����� L@b�餒��b���,��p)nk�ԅ=g\9�r��sE��g�!i�}!���S��2k��v�;�}^Ѕ7{vn��o9�MS*���'��od�>AC�Ȃ�X�}N�U�C�5�qC\w>�𷰓 )�J�$y@#�
��ɊQ��q����k�X�����|����7/���h�y�aW���KQw����4�vz�;[�Pq��
���o�E�ts�x50�U4�����f��:�����~��QΩS\�������̒e��.y�H?�ĽP�6@ۣ���P��k�\9�y�"��>ѧ��

�3��"v�f���pmt�v�у�z͟G1�0�b��������$�:.��gx�K(n��0�/;��oS���B���σ�����彉�y�l%��{u�J{�[T"��N� RTUie��):������ $�v^���N�R�i|'����L	8�f�\.����r���L��m�ˠ�������D�K��O����C�]FM)"jEŢk(��mJN���a?������ �MT�lJ�Co��Q��f�e�c�q�+��[��#�t���~[2V�0������yglW���ۃ�w��N��i�x��r�NV����&���<��(���* yl�g�/P�ʯʅ�9���L�L��g_��s�����ӑ���r�{q��?����xoɓ��v5��{��]�D�/3_47�}�G��+ѯ�����!�I#������`	�r������Hf�n��g 2��<@�#�g?$�ʎ��
�bK�E��ZW����;`1!d�re��f����{�.���i��=u�G4;=�|ky�׶��uJr��@sl;38��93Z*t~�\Ҭhy�~��Q��E��f�H�J�������N��>��<�g��<��Xi�h/���I��@���,Ԯ;�'��>em�������,z'""��Z&9�I�z�G/j��K��z�s,�*�����+�)�Z>�&���k�����M�F#M�� �v�%��ͷ2�ٗ��4�������֨ȍ[R8��ܤ.�
�����8�d ~A�X��ʀ6i�}ȼ�Iv�G!�6�( Б�yz���p�\o�(=�/K<%�[�R{ny�+�z�`I"�>���n1�V���~c����)I�i#�/����{�g�ĭPHW#ݱ�?���Ѷ�s[�����4R�����q��ö��(��#F����[�/�ϣw�f��l3�a҉����	� �Q��d ^{\�d�n-�����)�5dU�Dr*v��JwqKu�AE�l���2�qe�;��o�����gf���Ɠ׷����X�R�Y�N}i�_9ά)�d�S�5*�RA;��4�lv3��r�3��d:��b��}��=�ٲ�����l����ا�z��O���E�� ��	ԥ}C�I��]�� Z}�L���=�NC�t�,�e��)?��ė�-Hc&��	�Gx�M�*-n����]O.�_��j���{��D��2��H�ED�@�=���@�Z��CA|)��`Z;�ʋ�\E��\a������<z�Ӌ�M��~��J"J�.�+�8u>\�KؘF= ��7z��R:4�ܯ��'�?n���D:U�>,�~���a.�?�mBt;߂�����LB�[q�:+Ix��=��`1�czSu�i*�n�z߳�5KOgCu?�rΠG���G<�D���6�{��'a�4���D�!zm�����H�������pրP"0�p9�+:���]�o����l�}����BT�w���'���)�(����A�P�X�������ɧ�g�7���`�@���@4�Œ6����m?���7��bD���6�|��]�8�M��*TN�e�wJ������To�7���-�Y~#-n*��:� U��?����E�5�l�=́����}g��H�$W��d@v��o~D�F]�y/�2���$�<)��b��v
�YZ�6E.�l;�Á&/�~�2JH�$�=�}��
�P˞�l�t�Fr�����d�4��g��o��<o쉟���}ΥI?>�� �|�*I�VdސzI���R����B$��A�M���z>�⿆�1�
g��d}�&��=A}Uh�ު3�آx�\��M��C9Tw�h����-LQJ+Ppv�b
1F�(<x�ͅa <��)�G� L���O����XZ*�N�wf��plf)�f��D����HBY�YYY���4j�]�W|�W:��m�;>�#oh��̖��N��b�r4������s���2
�yĊ1g>���%Pw���'�;��V9�򪥑��.y�P!< b����Tu� ��Ί+�f����֩���-�9g�6��y~ܧw�l��{�g�.\��ʝ��H
,-8���G�BQ|�pn���#|�R�,T�4��J����Y�8��T/��Ǖq��랸(S�c�Jg�V��O�����z��K/k>����N�K��a��:B���{�܎��0�>u\���yۘ��`&PO:��b?{� �P��FFǃ?n�D��Y;"�4�,��+�`U������/� oF%� ��T����\��n���4��Χ�O�nWy�R�K�Nj�"/B@�v���E�����\�Z���@sϸ��zk��uߏk^�oE#�����\�bCH��ċ�n8&�6�f�K|��v|�-�ˏ�fb:St�9�
�k�{)aMS�)�1XĞ�Yp�e�b��+v홯��i�j�˻ٱ�.����:�*�>��q�֐`�?[g}��u���^��S�V���h����l�O��l7�g��a�R}T�Ŗ���nC��-n��r�<5�W�C��8]UN��:��b�ߌW�ʞo|�u�7nx���,���)�&5��7~�����^X|0��.T;?�m ���cR/J�,!�h�	�m���x����R�bɹ����z�C���	s�<˂'�g2���1ŷy�ckr���8?#U]�i%�H�m�X��ህ �~W�3}:0/�ci��-��YPC����!q�V4��&\����x����%�ƮQS��V�O���PV�?�_`�����50ë����:��Y��Y��i��o�Q	2�6-�Ͷ���>;�w�R��Lӈuv%)�,��h6�"��PĕIwD���q�z��v��ބ�6O/�u�#�\B�oV��`�2|qn�����~\p���l����.�}#=t�"\"���44��i'^m�C�x(zjۈVMy�%m����`k�6��-�dp��Pb�-=z1<.�H�%V���t��<������*��W��$i�u����S)��_`v��$��+�����\���2�K�k�^c�I�ɴ<dr!�����ڴ�������m�<�CUW��>4U?xYZ�%Vig����vj�}8�30I b�
�Ȱ������wkp��J=�A;�Q���K��i�[��k��Pld��h3q+�b��M���޲��)�@ْ�Y�7�0�9�?��V��o��8��h��b���6�A�h�`Ԝ\�d�y��SN���T��L���u[��D�3����(�lƧܨ�z���1;���v7
8�I5Z)��u��FCH6�O&g�SJ�OO�"�6%��6Xc���ħ�i�+=��-�d�;�ͅ�]������t��⍈�k9���	O��3oE�v���ft�F�7"IgL(����!a�:(��]�����I��{
�!�ҹ���L��-�{1\ʄ�a�|��hITEY�30��j)8&����o�5�HT�c�OLB-G��AF )��O��pv�
'-w5W[x���p2�<'�w�`4+�"o��-;������MJd���y����y׶�ɽ�ҽ���9Ic��/ۃi���L-�#s����� �DU����s����q�t���q�3�zd�k�����_�uπ`�t׍�������9ѫ�m����8������^_�yC�e����Pq��;�ac��%�fid��dwz�4�#FLd֯�K��,�3�P��Qac�Qz�x2[h��p"�1�+�ʐT�~r�v_��U"��/:����é�-�5˘Q{)�uq��#ڃ����-U&��L2υ�B�k��Z�*jO{r�#[�DN!c{,���s%g���Uv\o�e<F��:�B|��U���(Ԁ�P��Yw΂Z�Y���1���� _��g�S������b��d+n��H��Ga�D�� <�S��5��8zm�􉬘�џh�m�;*���~to:�:�Dj�(带~��Fw7`1h7�iQ�Є���F�<�*�	�pI�a�c��x#�Dv�_ǕݯgZU�X��Fv��k��/��F<�,���1f �\i�g;�1-'*}P��X#����5��1��G(��Z�wc��(-�;���HG#ou��������T�׊)(�+��S��#d�K~��~{{[�c]1�K�B��2 �
�@��xn�e�?bZ#Qp����ϒ6�gnNKFF��1o�i�.~/��k"��<\	�����-����'�c��������&uI����9B�y��;+�KU�u������	���sqH�����Q~^���D SzB]_WO�&���p<��A��+��(�С��Z�ϝQ���MA3��gY�Yx�J�tĳz�M FD�z�s��!0�wmm����n�X��!�i��r�{r�o�}��z+l�A�,�.����vq��{H��Y����W�d#'���GP���멼�
K��㧛ϛ U��"}���דz|s�tU��NV,�|���K&j�:uwJ$%��x��5�7�v��$ ��s�Wkk&ߺy�cr�/b�}[7eϲOt���#R��@\m�5lD8�TY��a@Tz��߮�������>D޸������@����+��f����ڲ��G,�=A�����g��z-�M��Zr����N˜��j�ŏ�v#x�.�B�Ć��c�Z�:3��vY�]�t��g��5�e觤|�&*���Y�҇c���dЧ��5M�(��:�q�d�B��;KSXG���fw� ���Xi���Mo0yKK�Xd��.#�z"IQ�}���w�y��\2,D�K�X3Ty �zӀ �Je-Ť]�ۉ��������c�����V[J�3yɭ�Q.�r�$����u3	�qN1�IWL�͖\���KbEa�D!�ZL��,��z����)��p����.T��RDX��+�'M��M�M�wX�D�9{y��ơ�D���R�/��V�3^7��q������i>�4�W��49^�H�Йe]� �*���ܛʕ2�ș�=�E��	]?�>;.�c���x���A`�4ʓO�'�3�.`�r�8�60_ȼ���2��ʲe}Cu#��61W�*���g��U��CXh\�EuK�����w]_o'b�$@J���aWbz���&l�,8^�Ɇ4��D�I�*���Vr�Ʌ�c���ٙh�˜\�&�8����������p]jv�yF߬iĮ\VYe�8U�����N�
&��S~0��3�(��C�����nk�8�?o l�Z�e{�i��8w\ۥ���p$nA�ǜА���(�]+� yvqɯ����Oj��:'ה)5�E�ѭ��e�S�mM �j�EdK`�W?���{]�g[����4�F����k'��|���F��� /'m��)�]^����ǵt�L+�,U5�%<8ևα!o7g�v��p������:����>�E�P6�M6�+��X`�������;`ХR�|f�\�y*Ps!�L[l�+P#��LEn`�\���\F�>��o]�I8�����'Iw=��CN�0n���
��]y�[���ͷc~��W թ���zS�#q��&}��J�T����]����P^�,���� �f2G���L<���?w!d��')�n�m#��f=h2@}���}�6U(��X�-�+�|�Zä�.S?��R����lu6F0.j������ō)sU��J|r��^��26g��BI`�wh�>{+�M{
����.��cB?[�᳖%;�������6�PU��|�Dr���|L��3���壪WdIX�^7�&��B���R����R���_����v�cZ=?��\E����yh����w�=�w�QU��\�Ļc�fG
���:;Wb�C����������6���U�|5y�~&Ғs.���sMG�v�[�TA��s�Kk�݂� V�.��Ǉ��%�=vhv�����*&�Ƒ�u���-�������K]d�9���d�.��/Y3.L��m*.?����K�����Lys�ȓ��l���K��׭��@P�T~ GP9gQ�C��=�gdZ]V�MÑ���b9�9��"�;�ƍ�c}=��B"e}%��K������j��F�X�g�;�S�g"�C���G`X���v?��$� �D��\�E�?tTB�y��r@��I��V��
��@�rN� #�\W��|#��f��B)<Jq���Cݫ�	������W��CUZ2��9Y�p��o��l8�p}��p�7#A��sS�B8�/�\�@<q��r!������ϝ�՛ʌ�>������
Vw�k������;���b��l9�|���=܂���VMy��Ѯ�u��K1��vS5��=��n������sܵ�^�;�7Ť�W���~pŹ�+0yC�!�T��ue���xx��zw�Q��4I�����g�m��6�pq�)2���ma�&(a�4�ީ��}���DV-#W�۞�Г�s���w"��.x����b�mu��0Z���w��;@I��?͖(.������q�;,�u�/3��y�qQ����a�X9�ȡ!Yf0�w�{�Ҭ)��@^;]�NZoy&������j�@�L3IEA_a5i
b���A|ܞ��&Hٕ�7��-(� M&��ccw�[%g��Ҋ��������~���9J�ذu8ΦwK*e����ɕN	����� �����v-���*�s��a<. k��a���z�Ou�
Y�N�51����(*�p��&���J��''ag(�/�"W&X/ʕ-�M/ֱ�h_*��TS���� U�l3h���^ ��a~�?7j1���ś?�3��7~S���"E���	���?��H�7���B"If�]Uod'������[�`?Ⲓ��6|�y����Sg�'�Z~���t]�V����swJű{M5NĴH6��'�wgd��q�j&Uɡʷ7�5��eɹ�Uۑm�Ng��I�O
d�p��T.h���ׁD9.�@Fq{���h�ۊ��Eq���f��h,ӵ^4p�2J��c샋ߒ9�,�e���Z���;�zG�R4�r��#��7k� �sl�zG�}P��Ͽs���(���g�u�0�̣�b.����4`pr�����	�uk� ������^/�CC�5�؝�i�a���&��}{<RGu�[zL���8ć\��2sv��v���W�����.��GuB���ze��)��U��Д�k��v�+��;�-�bx�j1�cn����[2Ԝ���'/)��������u
ew���&����N�g�Bv�������#�j,��%� ������lW��O4<��%��R�%�o߾��v0h7Y�����_R�$t������f��1v�c���f�s��ڵ?? r˞YR�m:_"���n�k�!p�j�SgUUz������Y
�����j�&I[4�͎K�*Cݘ�YH�T?pKnrH�J`tCot#8�,?yI$�k�Y��U��m�_V��_��ηd�{�皹ā��q>G ���4�N�Y�j�O���Gvu%�\��kvp��E�M$��h��wHO(�H�_s�A����R�:�8d���<�xϲ ;�;��h����Dr���WfCrx�wF�՗D�I���;������Yt���bH�'3����+H����TĜ�Ϯ��|��B�&�/,%�����N�7���E�π6�w��b��A�)0���}���\�r�$�����:�9�}�T���O����+���ŭ���:�7ܰy��;��ud��W:n��	z��Q��A�]P..�C����o�1�˔9du_!%jcQXy�'�ݱ��O�ճ�>���%b��_�Q%�8�5ݬ��'^t�x(d����y7	����o��j,�/+q�ɂE���o��>>~D9/�i�X�P"�����,��Aə�/�s��͜:c2��vŀ[�9�iB��*�+��{�+'��]�O��@)"w��cs{���K���eg~���Wb|�&,�q⯊�0�2=��
�tu�ق ���%إ:�G&<	��J��X�@'�{ϵCƟNo�a!�+�s��3«�vn.�3��*�Hp���A����V�I��6�Hi͡��5�1K0�g�y���XmK��N��!�F�{�GvH�9����u�� ?>�+�9Bj�ύ�vt�����7U��M�rn-#wZY)�A��=�3��RYC�؟�pE]#��6�R�~���wӤ��]��y�$����/��z$��#\0l*i݂�tʊ�\�c].�`,���,����|e�0�� ��{�s]1[�#g��f9��5��Fn4E)���I���
q1ֿ��4��b�<��Y�[^.CD4~�_�����|��V�)�qҞ��Dpѳ��K�В�5K�U|��I:�$јmx����2.������JF+�z�BVs���pS?͈@���K���=��R.��;o�a�^�4�O/�J�bO�Na�����m�㉼�mA�����꺍c�E���o�wf��g��+�������T���������;��O�D�����KR��΢^dH6��Xe�`�dR�xMjkq����w4뗬�����KX���N,���6L[���R���I���1��!]�{Өϗ)��[����*5�S�n��]|� i�&��q���hȼ�5���g���ıX�#�q�����qWKXH����Ue��9���rͧA���|@VcD����R�VV��MK���VP[�k�'2w2�8c�T���x|gS�-�t��`�"]�(z�m�����R��Ē�PoD#��y�O�/�J�$�,�U�(�E�sƩ.^}�~J��=Z����yʁݛ�8qL@�������M��:+�N���P ��1���\��NB�c��-�h֤OC8A?r,�O9ܦ}	���9�z���*/�R�O�'�3C�JǦH���&�UM�
T��}��A/��&�R�S4G)�>�'gh��9�-H�)�g[?���8DM�����H�ܟ�b�Q\<ݒ/�1k����Җ��'K�m	����
ɚ#�$�w���y3U�eKb�;W��E%T<o�W�� ���u�ɑo^�<�U$o�g�	ң�FsR��6�H=d~�&��Y�#�	��HĊ��Um����{�8QTe�Ț�o��*�i\���j�hڤ\aO��7U�	�>s0�+�u�^���>>긄�u�N��8l �Zͫ�M|`�����ôٝ��S��v�=�p��i.�Y�^���)W1�'N~�x�>��en��|2��.2��N"u����S��'M4����	�S�"� �w:���d�K<BL�T=>R��Z\D6�(��$=��C�~�7�_@J����d:K���d�����hL7m�8�Mg[�����"�6�P]*�������O1e����nB�8������[�	�i-��쀫�i�q?�[ǯ����J�	S>��J���e;i}|�,�_2�LR	=X��a�����F�I@x��Ӄ�ܞ��1�+T��Փ5�z�I��h[�9UB����Rw����S��T���X����'7����"����z%��p��v�Q���Z�����C�%�RW���M!e̓<��
=�ȠZG/����MZ��n�PE�l),K8���d�N-ķn5C��)����_"GqS�1��I>�b��?��󻕎�Mהۆ�E -ӲlP	�7���b���NZE�X|�3vi�%�C��<��ёI�vB��̠�L>
���ÉwP�Ħ���Ǧ���3sqO�i%o*9n~]�,�ȗqL���V���so��L�:"�,J5-���A���[��g��T�8	ЬB��y�
k��V��[N-R��X?$�@�R��|Y4��@8��s����&��$	�Kģ҈<t�v[�=��NEUv��|Ę�=���gLґ?�
�d�Н_Rih�E��������sx���fP�t�D�̵�{���R��Ou1x0�u���<�sZ 9Φ������ ���$/���lzM(�aOO��D;Ԛ����z�(��KQ�������J�����ʵ�OS�R�������w�.��,�Z��wC��b�J���W�b��S3<�K��ӳ,��'���~�+G��:���o\��YO݋[���p�1�{T`�н�
�	��
��=�[�C<�83 �Ї'�	������D�2��N�$�7���(�z��B%����od �]+v#j��㸟����9L�M������9�l8b�q��"�wḡhBڕ��am��(��Jյ����Cm�«T�h��%[�"n��1(�����6��n�M��R�<扈�dvI�j���8�#��N��%����%��v�"��>��ާ"�Nj`��e��>6�b���Z�QA ��Q
y�+�}I��A$�F$L�����#�\�<4ou=i�Yq
ˬ�O�^a"Ɨx�W�^Ά�=�H�?!&Q-�8�u�}G��^`?#��Ѽ9�m�#�ކ�8��7���GTs��J��8)�Ֆ��x&k�ƹ����u��	k]N�	�$�<D�>��l)��$}u>����I[(<p&�Rfw|l$�Ou�V��VL� ��;ID��s�Ж2�\�����=1ٷ�)x��⣶�]���=�A�(]ҏ�*�cQ����~����ׇ���~*hnɌQ��BnI��D_u���fy�J-q���ߨ=i�GV�zua�����:L�٘nr[�;�܅�R�S�V��@4�0�;��q��>��x�w��b���C�8^IdmUzv�j :�͗�\��"�����Z��Dz��(x������Me�&�:�,��I;èT��5@��:mk~p�r3'Ȼ�X�"�+�!
��^W@��PG�IY�!�R��~MGxp�֥f2a����Ս(�;�b�����x�'�� 4��W\���I�O򡑗ƾbF��,�{���[�]Ȓ���${F�.��"G mn�Ԗ�z E�p�&�*{�^1��-���4���B�j
��ݹ���
����1��>cz*�H�4���娞u�:Ŀ.v��h0�ُ1�]���I��0���s�����g�c/�ޘN��g�(�����˔��p������ɯ�mڢ[���><�q�mq�r&C�Œ1���v��[<o͆{��1��^{B�NtP��R��$� ���(��*�F%��zX�;�X�hM��4����
_�C�+�����ބ����,YndQfU��J��b�{�|�)7 ���%RM)#Ib���RG*�:���ƈ�u�)��H����6����H�1���(����@�u��*�I��4��	�[͵r䛓�;��o�ܽ𩧒���֖�p+-����)5��Х�޺���ᛒ�N�cSSj��X,�i�㧻�����	��[�f�QN�|�:��>|��|�Y|������h̀���p���j���&	1����� s&��n��-��ͫ2Ǫxfd]?!��C���5�봮HJ�s�Ǚ�@�=��9;1�M�3~��+j}ۘץ�� �$7����)�~�z�����j�m.��5r�)�$O�|�z�H�vY�I��ˬe�xdvF�?��G�PaQJ0	�r�s�}RQ\���+�^$�r�lm�nx���]�щ������ﶮ�F����M\���I�9�y%��2Օ�U�7��j7�/ӑg�7�r��r��ۧ/ʥ��(Y{�h�$��$(���~y�轧�br��Pf7ڎ��{�*)*xt���.�Ǵ(�����lg:SH�d�\M���a�����ۘ��W�Bo��Q��&����{���H��j="�vEwq{�9�����)�M����`�ib��� 1z�h��$5�td��!a��`���R�vg�a���Jsb�ç#�_���,��IȦ������i��@re��hm`��$#�QPv�� Q�s�g�N��P���]�9ٷ+,��R%�<i���#�ڂ3i���x�/ݡ�%I#Q�=��H��C���lnC��W�G9Q#@6LӏS#�������5n*�*I3�[�FB±��J&Ⳮ���Q�F3�-=	R���n���r�*����"����?�㥾�ȃ��#�7����Ea��V��#h���)"{�ݓ�}Z#u��)�Q[����vq0;k�sPQ�'�j�k��a���=S`h�{}�B�%��hRA�G	s$�4ߔ(�/�+���T�
�l�Ò��{~~��@�7��&X�J!����b�T�ȯ��J�����9��%�%?��z�R���/�H�ĥ���ba-�,�	��!�$7�$V�td
B��6ь��f�V�>�}�ȡ �o�$�RXS�������3�?�R������Rge����������!oI�&k��%�'o�간c�5��{y�`P�8��'�h�|3�bW{�4����ʬ���4�즽��E/�]3����w�EkXV#<d|#+��OJk��IP_4��7���f��3�K�l�^wχ@Smx����ԕ$!�N�,�2��ĵ"u������v{���n_��p�ۡ��5DD���u��qǻC����pi��m���EHǥ|�>�쥪�ѕ}al��� j�U�#6������W:(0�R"��2��n��_��	���X�+�M�wb��j��\��V[b���^�~��]��(�{��fd&�_�t$5��^� J4H����š�����K�q�8_���I�h������c+��j7���Φ��d�P��B)�*�-�������-o4���~5IT�"��1�Eu�s���NxϮF*9ϊ�7�ςA����S����0z5��=oou�r�|�.��/���]�5��GqgH`
�':�X��i% ��`+% �8s�2��.{�]4������d�1(����z�̰��@���v��6��,�ʆ���:����=B�t�~�KG�����'���ӂ ��������[�|��^�!K�7�)��\8A��[�0���v��Q�@4�C�B1�����e$[_P0P��xb`����"�19���}�U��� l��'�R��[1��q�`�g5�����y���xV8��i���=�|G��,��_����A1�MD�����.�_�l���9h=[�/�k����oF#7��>���,�������"sФ�����SH�����ql#a�Hٝ�t��H��˽��%^���T����7����������axkU�2�U�/�����,^]˖UōsY�w��ݛ5r�:V&��p���5TBۡ����J�4�_�}eT�k���H���tw��0t� ��5�����K��i������������]��t�|�gֺ׺��/���{`�)��͞����|jޙ4uz��d�}2�ؕ:�f|�g��O�4RR��$��h~x|dR!k��vc�-D�9�H���1:�;
�J:"
pN(�)L��T��պ����+�7��u4��Ű��>ۈ*)�D^JS�zewo�'j����Jo�u�T�]�����;xy�����]��]̷��̹/i9�/�/�w��*���ǉ�C�5>�I����s�L���U\�ql5m[�Xf�`�R�����)js�]^R��B񙆵7ƈۡޗY}1L�r��)����.:6*�t���Xܜ`���SQ�vjI��C�N��s�y_M�m�hm�6��{#�ֵIpzR �>" I��g���\����v+�cp��1.�ӆ�R��9Qz�H0�VmvT�v�9�ӳі���*p.82U��/V����o�Y�� �qR ��@���o6o�;ր2d=��}� L�lit��YQY�8���Q�Etý0�d$��̳J�P���!�Hn^<����*�)L�@[��̍�:z*�_aO���_5��;����_�L|���PV~شw�	��������3]�:�K/!VYP�R+x������j+�FQ^�c�B�����ԽÚƸrL���X8O���]`H@�2N	Ln��cT��3��:��԰'�n�}%h��:�գu��Y�Υ�=]��oPO�Y�9����&D���M�N|�0��)�b�z��� �z�|�dfe:E��<��	��a�w�$���0$�.9	�{ؾL����t?���>�����wՋ��A��&PR=����~��P�<`�s��X�+�Z ����A�ݷO�=L�z��Ԫf�����%U��o�c >�˜�o�PSBj_e��O���9���S���^����Б����Q��U�[Ϡ���P�A��	�K�����p`|��u!��w8��EL�*,��j&��/�tмjo�P~[r��`�����y�����zv�r����@j�8��+N"ƭ��i��kn-u'�x���~�U��c���i��>=f渺���P�<��c���}��	�E2_�B��sOl0���\o�q���= ��"��Q��<p�/�wi$�ҳ>,@�i�,Owr�FA%����Y�»Q<��\��r=��,z�q�p�zo�����np����lZ�y� |�C��fb�K��(�ž�Z|��#9�b�����S}C9��eƋ.D,i;����y��Z�����2Sx%{܋�p�+�4&���/6`k
P_��-`tИ�#ә�2�T�~"�f�^Ӛ��SG@����x�lkjX�J��5,���S_� mZ��۰��d8o������q6Ji�HCm��uM�ÓW�WoȜV���ܽ�3"`ȏ����$����մ{j��S��O6�|+�}q�b&�� |}/�J��߮6��]G5Ja�'̘w=2s�[��|������`���k�ȼ(
�h[�+�mY�]�]�Kl�L��~܋4OA��єG���$e�)���%����|}�G�)�%#	�e5��.A�
=��_3�)�1،��&e�,�a��
��!X��,�H]qV�٧���xL9���?'�w����-e�
H#�	uʳ(Q�=ѳ��'��.`���;���iK�a��,l��+G��m����%bRN��Q��P��!��y�� U'i�VQ?�1E�#y>	�[7N��Ig�1��&��=������cwHj����J7�7�4$ԅ��j'�e�&y�&-ș�i�3ew�� $�n<_��l)^������:����R�n�^����V���<Ca������|�����g)#�1I|e���|З`.��m����Ý��X���>8�^^Q��Ƥ�I�ɥ�H�$KC���,��c��bO!;ƀ#��[�m�T�������Mw�Tt=�VJ��s�g|-v����ʹ��R(��=���G�E���?�ݸ9��
ZT�NG���S����bk�({Or�r��_^g��Dɲ� ���j��'�Օ��~��C����J�;��r�ɒ���LG�$�7^�+:��H�ԭ&�O�����gf�V,�:�Kf!�A}];�Sd��y*��^�n�W�Z��7��{m� �L���8m���� q�Ԅ
�ei�
���C"/v�R H�Ȱ͒����r�8.M���!�]#:�@�Xm��V�Q��"�˖�>�zxw��3]A�p�}u0�A ��¾�~�;��j�g���Ǩ�Jc��(ⅉS�hA��Pfֳ�<y@��%�'מ���rM�P��-���n >ƃ�Y�q�7�[дV����䯋\|�-q�$O[�J&B��^��u�<.��GS?�= ඩ�#�2�
IN��k�d����u�xu��W>����JF�T[<�iX�,(r�H�]^�R�y'B�Q�Z;k�M��Ϣ��ٺ� ���A��;�uQ�Pf�!��Hп�ݴHv��ʎ'��&��7ح#�YXc$�Wt븟�G�~�i�� �]�UV������V���SiΚ��^��	�&3m�)��r�
c灩���Y<��4��~���὇->�6��Y������NA�:�c7�l�-?��d�V{��v(��4Q���4�o�,�^O2��R�{�&'w'���=�2jlx9^?QbKHvQ����E��}�N���_E^���@��{eaDǢ`�h�"��'�ݙ�<'7ػ
���0	q��.Q/���ʜZ�4��Qe����5��]{--p�(�ГǸ�����.��N�1��$���;�s"�<�u�y�<�k��G��:�n'n�}�͆��j�ú�#��ʛ�B/Y��B#����X3z��P���A5�#�����j;*)_�FQ�����%�t����+�c����>��Eo���u9s�e�-���2��x�$�8u�����덉k'�T��!�%br��F�ׅ7�T�=��+JL�`r�c>F��,`&���MJ ��1.�x&3�
fVV�)�{.������[,��红�		rOP.{�1�.X�>?���"����ڗd��]~q���|r�G@^M��7�[°�����t���dM��ʃ-w&��0�nO8A]Н3�~�_5��4���j~��E��/�E��|g���vº"�H���P�ş��z'q��C&L���x\�LRs��m��D@���Pg�kn�c��;J�'�S���\�S`����EK��I�)�� �9��}��=�|���dm֑�<����}�{U)3T�TX���V��}R�T8P8v���Y�-���d_�s����5]]�;���D���8��=�y�zxCf�4��OI��O
��2�r�D�j�7�t1�6w�r����PZ���È\�b����r�\�J� �I�hh{Kħ��3��c����f��3��>�TQ���X��F��k���{2w�N6�C�ڽi�9�_����r�_�~�cK�uq�������Q��}�dq^S9���=+��H.w��*aޭ�5�ivv�O3�n�</���"(�`,e`nGr���;�HղKk�4Ծyϕ���ĭ���v7M�Ұ%�KDd����N���X���"��s	�N��}�	*��7�,a��;f�޷�}���.N �ɽs��E?����ܲVe����]x�j'�"��rfc;[3ZH��_��L;dh�ۂ~�	�M�$�$���}w���/LZ8KII=,��8����j5?]
���vf�|;0����s��9`Q����vJdeЧ�u[N�L�w?�I�>bPR2����j�� $�Ca�ƀ����N�K�e����仼,6�)�cuf�kK�6T���8抆~�U'�+�J�8��OV�VD;p�����C�P�ḟ�o,�M����.�����Q���:f����b$�������{�DG����qUliaJ�G���M���?���������]V4��2v";'xu�@��侅���c�AS/�gQ� �����Zφ
�#�I,���oupu����g���&�-Ѩyʄ��"�uZ�&v���A$a/l���dǳ�N!�0������)���5:g���1�zx����z4훪#X/�4K�T����τ;�.�[�Y�ǫ�T�]��F��$���LN�s+����Į���M�x�ݶ���!%9�Tot/��9>s�qZ�o���k#<�S�-�Gl��:�e3�,Il�-Vw�a���U��zW�k�t������k4��N@����k���,8�n�v�^(ZL�Amb�bH3����ߛ�Zc@10z�'Xy�=��J��v��'�U����J+2����cC��ި�# K ���υ&l]�7� ����)�8K��ua<8�?(��g�ng���m�G�YFr�uÓ)���I����|��uu9xY��v�����)���$��S[�$���?CH��&���S�1�N\�m�*�.QF�=�гM4 ������{�f�#���3�/�}�0�Iy�6���2� \_�L �ܮ&s�b�;�01�+���e d��^�qׇ� 1pm��M�����`���d.��rzJn	3�Z��nЌ`7�K֭� O��*8���w�!����.��5�/"A�ҹ���+�p��<˳���M�i�����o�NQ�bG:$��z,"���~��TzS�ѥ�)�tks�D�v�^�K���1N��}��$����˹�|���6�����g���NA�/Qo�	�������ݿ��Xӗ]w2>Y�@
ue�c��D��$������w<7sf�j��8Q]H`���������T��/P�DF�Q��z@�l9�l}�Kl���!���C� ���{66m���[NK�)�������Jf�S��Ii��+B���\�I҂q@��V~����9�nQW[�ʀ�=��:���''0ʃ|*')&�C�e9������m���f��q,�^�N�|1��V?*��Y{��>ߗ�|��r����K3:��"�T��/a.	0�u�1h�2}FR��:�������(��*燄�;jR~����Rm��%���k�b�T��)��@揎<*8���*F9�+EX��N�U���|l�%��6e\ )n|��|��!����@D�W�z1�VK�/�)�|��Ί�zp��z��>���-!wD4p�8������I�bO�<~$]~���>Ҙ�w����k>��;���ό~2�䡃�_�H�A-��Q	���GH3�PX蚻�6w�9� �a����}+���g�� �ܷ��V�ή����!���]]V!+k+.C���L;�����Qj�Ƃ�cR��Ɯ�6[�zk-��m�j��� �OE�8v�F�dۼ����
�	.T��d��R�9%�(0��7�J�.s5޷�:��5��M�8���g=W�i�CxR#I!4_����za*P��DAq@�Hw�?����H���w��-���[��8D��֢v����x�YoB~��A�3Mc���/��3'���S�l�,�MA�e�6�t|��<�w����uZ^�c>r���ERi%C_ȷZ�B
�%f�t
x�����쿛 5��#m�9A����sS���
�w�?e���S���U�xˣ�5�����鈠5����}l��l		g�͎����T )����a[�V3���;��C��L��l���Yd�dr�@8& &�^��>������r�IU�A$>M�避&@���Z����S�u�Q l����EF�ZgH7��c���|��wZI�����ds��,���yl�=�������D�7/������(V�2vh���s-��}��I��&9��c��1�������1�Z��(hܿ� ���!��kVE��d�[L{?/�:1�g)�^��DG
Q�td}8�KL�j������w4�=�$�̦Ѕ�����:�o}��醎v+��f(�I����o�x�;>dh�Z��u��х����xg����H���CK�S��Z.�$c3,###��l~�}���-�*W�J/<2����-�Qk�$jيT���Cǋ����jzy�:��ͽuL����8��@�&$��m1@#�W���[�����n��J)�X�Lp���ڏۮ�:g��v5���d&&�b�ׅaÝM�N�-6e��b�7���𐨽�{�虔O���Ҍ�����E�&�Z�L��Ю���WZr*�[�I�������F�qВ�Y��R�t`��R��(d���U��N����h\�oޞ	�+�.:�~�0'E�B����3^g�����佷�y���l\�R�������c��8��	�?�W�B:(�
��u9~�m�~�eK��!�YG U{_�xC�y]�ˁI0^��>R4]�����gP���4m�4!����Σ'76:���l�#G�Xt�ŽŬ�Q�j�<&�*�؅�y�"��s���А����*o�W�A[����/�6�@`%I��z=c��s�������jg{p��N�,?��+�[�>�����jRe�<��̶F��5���9�֍���{�xs#&�^���T�6���p�F���
9s��^�6�R7��v�0f���&���wW�Y�W�mNg9ğ�d���-"�#���S���L8����ߣ��;�X�jp�d0g:H;}q��v��$!�̠��m���H���S�⣞�U��W���%��=YՌ#�
�s�&�P��Ho�J:[L�� ���s�����a�?�/������R'n՛?f����|�[�d�m�G�@�w�z�I����$(�N����r�������ˑ{����NV�Nj��4�!P�RqàHx�Pv�DX4�w��y�
�0J�w�UBs&a��y��F1�9�Q)����bxr����M�:�Lj��>�ǽc���$yЊ�H����@�����g��6�n���3�j��`-����Ө�j^�� �o�P�M��6�ډ���t��Г�r޼+.��s@"���f�͹{̕|�b��h.��O
�o����'�^�@��TiL�?��۝Q��{,�/!�]}�J+J� ���?PK~m$B]  �f  PK  o��U               word/media/image7.png��uX�K�/�	����'��{pw�����Aw�&�����6}�{3w{Ϝ?x�����dU�d�
��C�Á{�������w����Za��>�y�z���JB���[��*�w�������������~��Bո�'���
�w����"yL�ELs���8��4��Vy����~$��WwGR��v3RYD?��p�T��J ��֫��ZU�����<h~��>ڥ!p)��8�Ry�����_���J�� �����h2�o�J�������k�<e��W��������3�u�c�ǔ�����L{;��+3�nA���KӺ�������8'� d⊛�ژ��	5yy����^��竟O�ǃ�t��9�{�;��r�x�?���a��"���3��qc��a�. �]���{��5..(�r�8���M9��[��E��l��/�1:�=��NH<�K&�G���٤���'�H��������{���E�#]��A�����\9C�};��)���L������ll����(Z`��P�����9�N�����Y;��1�����j9=����%6O�9l�z,��mn�~�T���jt��b���ί��9҇���«d=P�9-�M�o�ߏ�*'�rv��D�Ce�������:p�3--m>�}�����Ź��E������æ���\P�lFB%�"c�9Y�CoK���?��8[n]$�ڕ����f��!˒��#%-5�/K�������*�K	7�������:�ܑ�Y�_�_?�
�]��8�"��P-Q.�3�YU����/��U��b�h|���a����N2�����qp�Z�qf?��z�������d��4��Ý?B,>>��qㅄ�9�y U��aLYۂ���A�pI��������уIK`7Ӊ(�ђ_�$��0X
>��Փ�Y~��#���#�P9��U�[�̺#���w2��FT�_ �)ny���&c�ϩ:�,T��k�QN� 5N�r�a%����m��������
�v,�l[��������HpD�5(�U�{=�#e�[e�͘P���o�-�����6���G��&�^��(tͅ|<klI�q���Kf�8��5;n쫰�@B���1X��/��p�6����-�����
T�
�ȿO�gц�8��e��T<a��N�E�L�?Rzc�xL�	A��׮v���˼�r�os��sm�הZ�����dNK@<�@=��\���%����1$�<8���C��ۻݦ{�m�yrO@���X9�gG�͑�Z�Eo���Z�Ŏ/ ������iNE�3�Vu���g��)n����BY{�ek�>��ĳ����s�0G���LU#��� ������4�Z�5��E�����o����F ��O	�`�:�,��u㜍�dV|}���)��]��&��[����+,��ja	�Qn_:t���3�Z�W�vu2z[�w�I�uH���f+�p�Kw����`�,�D��Z��6;��m)S�;��N_<o%�G����K���qq�+���OݸXRM7��h-�\sy������Y~%{��O	`�*-��q��F �#�|��ܶ;���뇋�l�w 4�>��iO0�ņ��G��c�ߵ�ʶ������]9�9�n�ν��6��VH�o`^~�Q>���0qx�}b}Ў��0����ϦzX�攸nBO���e'�ޘ�V�o������r~����MO7���Cq�*��u���ѕ��LG�E�0m�|�w���7"g\dy�|�p�b�Կ�iD�L�e#h�e,��y��̮������	ۭb0�'��b+i���FY��~
���+oOu�S����)z�C��F�'��GG�EQkP��Y��J���\�u�q�s���E�R���������ׇ5��l�\I�x��G�����V�دrȹH�'˸^�أ�j��	o�(q��R��)�n��zju�9����]J��֭��_�6��V���5�BI���^g{��c�F��'v�1qR1`�pWI�����EP�{)�C�px�]A1!�*�� 4�θ־����LE� ��f3w$zx�y�k5����3;o�;wC�ٌ���ᰀ,��=���A�r����SsF���P�:���C��i�u;ኩ�O� ��#�B�&��*���(�<;F,�w�S�\O"����!�{\Բ����Һ��" ]�و�aUя���<:4���f����9���S�ǭGq_�\��h�tZ��z�%Lߏ9�bR�?����0J]+�����T�X|��.���ZP��]}C��#�?���Z�e����ԠQ*)v�Sk����<�e��,�KZ��O��ppDw��@�rnG�uv�IM��A��_q�A�h=v��ȡ�\|��MrE��H�]w�s�3�QG�	-�3���ȬH,���NiC��@��R/��@��O�y��3��}M�ޚ�_��>��'͹���
��e=�=��P�F}�7O�^ܼxPeG_�:�C�$��#��HF ��9d {Q)GL�bo<�^��ݲ��j\�p�B�C��}�Ԓ[Ux�c&��F��@��GV�X#�&�N��6!�Ũ�7c�9����W�E01L��i�Z������s��u�'>��Z#�l)iv蔬��KC2wr���F7��a��=�߶�\�I�ҽ�Ή5N�L��Hlo�m4"U>��G�4{'Z���)�S��e�A��@hN���V��h�����>*�&��+_���23t�_���/߷��[��>P�������}�GU[?8VK8JL���|�L�Y�Ï�r���E�����9.�M�)t�bƯ�)[W���ԗ3�D��}#��BK5[A���-�+���o�1P���u�W�7���d?^E>ӈ��8b[@�2~�~z$ʻ�u��1���Y(3����:M<(�u]���w�N|�(V�m�'C�O:�����N���r�ɡt'A�K��V���\�A_�R�������kr\���$[	�LvVuer�[���q����/dcd�.M��x��y���y��ė�F�Q�A4M���v̙|�ҵ��p�q��Nad���>�c�����E�u���h��^�IN~�̠�6�!�*h����V��Ö*�
n��˯������*����I��!Y��	��'�Y�,��ɫB�T����3f��B�٥�L���=j��$"-��kE]�;r�Y�N��q(��(�L��=����|&�U^���<��	�2k�9+	��ifu4�� ��˼���
�!��6��j6x�i9L5�2%U�$��?���p��&��!'4�:�rTXq<��xENSo��]C�6���>�G��m�M_�֫"dP�U�ڕ��\_@�����Z����LڂY�)��Q荧.�ν�(u)jxHG~�UC�d#�6.���u�Z����AT�
}�?�2��}�w���N�����d��j<ܱ����Ն�+��h����\~�㦙7Fku�ﱤ�xƸ�$f�#�۳JD&�Fz\���0���)�X��2��'�\�GA��\��>پ�U����Gf#�&?��?e�wu�~eE/���5�%�w[�;N q�)����Dn�����;1� ��%��]�:H�SZ�D��跍���Z�1&i��U�sڄā���q]s�&c���1��*_W��P��>�Mͨ�U��}�x�,��k��S�~,�9:%BI�8C��	恾s�W`w�V��i��۳��T(x�����*�
Y�fk�_g���h���Eџ�-'&��]O�8�cM�VM�	[�ge��ylW��K��"�:u��T%���J���H�ɦv<9��]M%�q���2r�y���N��)�Q�Br.fNkܻ��ʩ�#����=�����X���%��$xp��*V��(%-��	�����8;r��l��$?��K�<17���ޏwK��3�W�&���`�'�Ӝ�5A#w��d�=�va]��ϵB�����I֗�cX �M.��j�/�m���li��V>��u�=�pX-/Ɲ4���E�i��co.r/�^�����V]�������g��ƫv�o;R=�ըtq,[�I�U"Y������~K\*���3��Lԁ Ϣ8VO4*%���j�H�6^=���	��S6Y��)�o�����+�.q�Щ$��h��J��=�NT��\��ᦽ
(�:�aD��v%�";�7��XȎy�Ŕ���N=rylr�g��խ�T�Fv�4�M��b�tDY8�e� ?K���?�.V��jWH�y�:~.��x���n���N����n�
I��ɒ�W��HHh����Z��kg�fE^H�&xpY6��
�w��#'t�[Q���a�=�]�#3�[oE;&�v���U�\��X�|ݑ��m�?#�ߧ�w�QK����~�b��|z���L�ɍ�xr�5W���MB:�D �#��Z�8N�v)�u�/�>�آ�.�5��H��oF��S1�Yb���7TSc��1l	����)���uÍx,JWЇӓ,�i�T)�Թ�)5y��QB�ċ]��̊E�&w�S���D����X᛼0�O ��ڳy�袳�pݲ��"�H`E�%���:�yo�s;�tm^\�4��V.Y�1���Ӳ�^��.W{�ҟf�2���H��=A��������*�ro�U��J!��:G���.��]����M#�c���iw)��M�j�Ш�
0U��֣��rJ�]�����G`<I�Ҭ_!����w�R&�5K�&�X���
�+aM8a�o�2�drɝC�/°O���]ݗ�gVRh�VNri�C2����%�Ň�����1�Gp���Z�O��`��׏6&��*G(��[�dD�m���фXɾ�S�V7�WMd�1�D�BN:/��!�����]�sq-��=8W��})�:�cw+D�h�zm-��p)@���m	�"���>\��	��_��<HJ\�!D}�F������TӸ�/�0�"�:�l���������rT�5����oL��*\Dj!}@\����4;��!��<��D�u4�a�I:)9Q�csp��3|\��W�}����aOq)��e��uH�we��hi���wo�A��e�m�����vl<_�!���V�~�oyHXJ"��r0���}O��E!�A�b�PO�ĥ3o;��`�&;�m��:Nbؿts(���tO4S'���ˢ��K(�(��@��ܚʾ��7�v`���kd�+� 4젨�9��'��j��<�G�3'ćH��J���X��<ji�NL������a����W�]ƹϗ/C�Ǜ��?ƴ�������/Z���o,�K9��IJ}�eL���_��EE�Kd��A��W	s��r� $�φ�9OX�PD��V%����S�Y�m&�
��E�VM��坱������.Y�KC���I��z��WM�G#����O�D�
�X9w��^��EO��xǢ$�}�W���k��;vQ��t����t���FV���hc.�kj��=|�f|$*��W@G�9�B�/�@3��9\�肎ơGD*�ya���� �y󜊵\�����Z�.]�Ʀ�T���ᎹP1!^�^���<�"@>��4Exէ3]8b�-�������$�oJ��>V�6�[�p��qSk^(8�p�s],w�`Ogc�jE���0�/@�\�	����V^��t"F��e���$/�9Wܘ�5��!��/�D�4�D�O�7����4���.�
K���gl�T�˒�V���Cu�����t0.}�8�IG�Ձn�$�Ìe�nE�p�N�і���>��@;#csB�3+�%�*ϴڲ	V��>_���j4!�{����,Wa�x��
O��>�f�Z��}����ʡ5�_n�r�7;j:��T�fl��eMXvg"��R��������p:�Cg�o��T�G�E�iT�1a�~�T���Σ��ش���ؑ��m|eo3I�4��g�Y��^��D�;����T��ĝ����ȁ�]�1뱢����E�8c'^-��٧�iT�����ׯܼ��@��a�٢�E_�[�[���LI�=ն����툺͏ʏ�fI'�9ۿRo�?U�˙-���.#<,c��]��p".�43U����ј��<�2j�n�������^�{��D�t�\�����7@g[S��b2 V��*�����@����Lԟb_��&u������7^+3n+�r����dl)�������X�(	�h{F���t���%��#�UJ������K�(,��P1�4�˓a}߷�&����̫S��O=�RIC�X�=�5���P��S����~`���9��"2R��XQe!'%���e���j`U���x{]���<��$�17ug���]�=����c��q��d�ޢo�BZR���a��c[�5υ���d��7{�J�uOI����I�}x�RU�J˨7�m�2�S6 ��e�2*|D	�]����f")Cm�F�K���
]��O�Ĺg�P�B�X���#H@ X]Kn�!��+}�44�[֬��~��|���Zi��%��jf:���W,���s%@ <W�I�{�f���{v�#Bs%"R�����k|��]ʕ�W�Q���q��HYk�/Njӓ(�5�%'`��ii"Ϯ��A�5���f�\���̳_9����-�0�r�C�စy��(o$7���+P-0�H�(����eJ�l?Gz���;�L��	�ƹ|]��zXr�kfQ�w�x���i��n��|�	¯$�ҳ��F���{ :6���[�JZ͝ŝ,2�[$����z���ܽē��`HQ�5p.���JS�p�Y��.���"����U{�a�yIk�l��sǺ��|��1ַh��Wo�eQ�캯��1	�f��Ef'�n��\��<����|2������$"��)���N�ʳ�W�qg	k�m)�W"��1�H�Ŏ9v�,.Y0!`����
ȋ���g�sPD�p*�O����Y2SX7���{�ybJ+�'�U���������	�w��,���"��W�VP��w��vI6k)�K�|9��\�EM>PZd���Mjqg=&>���Y�w���݁�\:��4 �j��r�$���Υ���m�+W'p����D̂�s���a'�ǋ(�}J�-<�	y¾ҦL� _&�s�?C�}^���L��",g�}KS|^1Z������%R��.�����sxj���I������|�W�+�����]/+��Í(L�2�Z����$R� N��oJJ%�ny ���Bg=����:M���5��3N#z�z���y�B�K��{�- �ܣ|O�h'4�1GY9�-����M��P�5}��D?-f�r�i�dz��灍� ���rW�/Q�6����x�8=��;�Yp��b��S����;�2�'/�Ƴ׌�Ϯw�Q4`�	���.Н��+����jh�g<0���S�?q4�ݶ�3|��O���Vӿ�:$��yp�F�v��N.�z
�OX�B�W��;�a�����F�;r����m�})�t�7�v���F���B��3�}��TX7[�]/�����K�h��1�պ�)����Q���ma�̢Rsyr�c�^X^�q�i<�l;g=���ˡ-���t\p��C+�wh=P����ri��?fމ��]��iqPV��
�MS���22�)f�qLh�	�b�v3P	���ɽIV2���B=�����BB�K��dʌL���޶�)D.zP[�������:A���,��ۋ~���6R5��(���"��gp~���H
`���`������.e�7i2[�����e�:��,i�xŮ��W.9�"�����6��������$=���Ř ��_���-�#�+���x��	_�ɭ�}�=�Y?L缟I�5^b�YS?���7 �5�#�;���q�$�V���N�>q�\�L�E�d��S���"g3��$#VX�)���M�i����_ V����Y�5��<s��c����g�Z=�u�vǆ�fp��U��6��|��K�B�\��i��׏�cG9�r�d��:^�$.�,��(�5��_�ӕcy\s�j�hI�6=����BT��*]���됞�W�P��\8��U�R��_*�@�*҇~};�����.��I�@�{���%���9n%�l���!�沏\���]�z�όޫ
6��@S�A股)Ӓ�b/o�;�m��ui-�5���|8%�P��D��x#�W,��;��[��=2�~�[����;���}J����!�2�R"��Ii��O��_Uh�
��X�^�P�E��m�"�[���$��-��mƏ��U��ɷL A��S��XS��R,���K�x�I�\�+��ek 3^n,
�&/KX���.�������R<���j��*ɜ�sX�d:l0��P����θ9��c����B�@d�y����Q�!G[Mne�2'4��;��s�}!��<��Q��jbZi91���r9�,H�/���� ��"�ε�Ә���z�LX�X�+�T*�i7��wv�aB��{�W�u���1�?=l��Vf����9�GK7)I� ���/��mI_1צJ�\��.�5!(�]$-e�{�=ۉ	�nڥ�4���o.-#�(H��GɊ�N�`�Š� ��;�����b�����ܙ�}��_��s��!|;
!l"�$=�K�<Zn/(����y��^g�%�L�D@Fy�C�+�����f^�b}	�1���X���sX-CT-S%����xJn�!�e~Jh�ow+.�L��N3�qUh�D�V�B��监�h6���VMVy��wH ��)g:��
e�>Ԅ���d�d T6TYԹ��̰�$��c�����2�]�Lz-w�zC����"q.!*ZKA��5��p�|�����mb��߆�!�Чl��@%l���-�9�;� �@<�#K�t��Y�!�Dg{x�3Y������<�\�����(_��c��+�R�$��u�y@����)G���qDzϏn��(c���l�n{"�][5ha�3e�uq� ��/?u�$i]�k��_�--]*��Ӭ�2G�d�I��`��.أ�R�1ň��=L�����L��ݽ�{�c�)�˹��S3�@;�X���Mf�ﺻ�5�|	�1I:!������Υ<�⃸��D7B��*�Uy��ϔb�KJ��Ěr`v�4�Ƈ�tUÃ�(��_I(��#�J�疘����q9��uH_�7J��t{�s��6�E��vc�܀=����7�r��:�<�+팋>���xS'}���p1]�/C� �,�,II"��{b��s�Uf|���مp|���|��jm_9�ӑ���֌E"-zbeG3Oy�~P�!R?{8�ı��u$��	����C� �Z]��\�u��溉 �0Ɵ��#�{	�-C���<t-j����P�b��O�}v�bb}�,��OCLW/P����D�u�M���@ݔ8v-���*j%�k��F���8z�yb��Y�ӟ�'�#m^�X܎'	�T>��fjE];�e��`���ۮ�[����:�g��������Cݳ�k'ٴ�;�9��)'N!�wPLڄ!�����0�'�|�f�S)��;7���tL����Αo8��Hoo����ʤ{n���{��&���u{�D��K9f�����p�j@�x1'���{��~��r���-��-�Q���}&���M@��(=�4R�d���i_�onrώ�vS
�h��#Y��w1��X���b(D�n
�X��-k�i�� gb�(�Ǝ�pn�QǑ�����s��|�-	�����kAT��	;nG��H~K�Qa:c��Ew3�ɝ�bz1��R&g�����$�b�C�����ö��V��qF_�L.(�k0��F��#0;��B6�{��%�����a�������k��j���å�"P620�h(���?~�ms����1��Z�+)������ 	Ԩ��3q��N/'7��ֵ3/m��H!}���?X�CI��'��\ B����@�[O�?�����I�-�:��q�eX���ȪC�3�N�Z&U-�b�l�42�J&���h@�h�ĺ3.���ffO��g������fj�"_j�ڼx�_d�����1��E�<I��[$u�~��5�XVP�������b�Ef�֚1���ڳՒU��,<����x�18DA����Cp����7Ȇۮ[\�Z��S�T�ڰ)�YU�CH�_iڐ3�Xۆ%�**�}1o�j���Z����Z262K�]]>?�Fܤ�L��0~;ͤ{�`Ġk��-a(�6M�N�0�>P� O�a �D{��ܙ^p���Ꭿ����"p���5QH,��C$�oM�:�\���L�	0�O�JV�-�7.�
�H8:��rhA�1
�=�A�ㆮ"wy[�L�W �����AB��,w_�����g�ҝ��x9�q]߻< S�T.�w�4f������iy�i�|���^(
���	os2�=eLuΚ��S�;�?h�}��W� /���dZ�3VΣ$��S�Y�^+�ɚ1��>�Z�^���\��ϡ��8�p%'��i���z�w��'q?1�#�WhvVGȤhk����Z�pSm��RW�?}�dwoC�e��d� �.��Q���0�o �ʙG��K����qt�Ս��K7����jz;^�4���2z��C��VQ�o���p�dډ�1�&�׊r�^��_v�����h��2A�������������:"E̓��Z���W�n�Bܚ<�(�RRD����5y���Y�/)��H���HW9o�!ɨ2�u���?f��*�(_��U��D�p�?��C��خ�������fhy�54φ�rZ�k�;�%��p8,v������S�&8���BDz����4���%���~��lwP.�uf�K�~��	l�W-��?突�bffC�8�=&ćg�k������,^bD�4|�-�%��\n}����0N��q�=�\Nas�GҦ����Ptb�PJe��T('��+�non��ݦ�u|�D��Q��۳��	+�ާ�����oH���|�AI�PSg1� t��TLY�2 *�j�����=�iR���� W��m)�Yy�:���w�ò���s�����A"�>7���E��������ݶC�b�g�)��+�-Ƿ�o�ć0P�(ؖ��q5mܫ�"�����7D�j�R�ʎ�F�"�B���U.��m��4t�f��0�zŉ@�P�^�VG
q��&�^�[�O+��r��˾R�n����q��>�Hw��=o�Q>��~����{F�")$sx8�������w5=ǲ��@ܪ���W�I�z-@{�%t���F�e���ci�9��(ٴ�ݎ@σ������b�����V�v�Fp9DJ�Q�S '�3���;c��&�����MJ��㛓	����<��X�<t��U����I�=]��d��ک���blN訯h��ȁ՝U�	E��g��/�Z;�yxQu��߳ob�;��Tm��?x(k.��ʸ���$�f`�ӏZ�%��P��ٵ�-?�Z�x�`1�4i�<��9O�^>��0����s<��@��W�a��w��&�ye��!���-��v3�|8x��<0�kᨶL��h���𳱪1)0~�a'�I,�����5�z �FHS�<��5���>V�����#U��Z�3JY�7���A�Bc&ӻ�F�՘3�j��Z�?�qCŢƴq����M�w"'{������k�T:|��M���*7Ŀ�����h�2�����l</@Ӆ����z!�J��%�<�*�����	��@n%ӗ����D(��(�x`��=l;�t_�^P�v=�L�4�����
JJ�1��dɉq�����E�ј����ы�QSP�Ci�O�t�� j����&.7�J5Hں*���4b�mXZ����o�Sg�R�"��.x��^C��0�TL�.��|�x�bxg�.���ae�ޑ�����>��c��`�Ģ_�`&3�FT][(	ǟ�1�p�E�+��Z}�G��\fl��B��k���C�������:�ɤl5(I&\s[<������b�L�e��͒�O���׎ż��� �}i���].��5�4����S���D�x���>N1����]��c��\���\A
�ϑt)�e�vPnxT:���!ӊ��C?��^B����[��W�$E�G�&�^�;���!�y�����
���!�#:�[���I���,�����<��_�coN~ԸG��\H������>�ٞދb&4�'4^��m}�Q�f)��V>������>����@��o�Q<� fo&�3HSal\h{Rw�檙:�lϲf������`����C��l.9a���!�]�c�
�vfjyQ�a:3�bq��������1��@��ﭟǒ��?x�EcWl�c�h�r���O&�|��GAr�%3��PKϞG�C�$�IL�c���5�ų*v�Gz3R�#���c�l{��G�O���&��?7�mG��$t+E��ǳ�,`.eL������er�պ�t4��ᛌgeΨ�l���@e�:���-`^�`&�(�Of��|���51K(f����i)b
�=_�:k���r=}�o�Y����l�J˝2��;�Q���x�s�ؾ�����x��竜�O�^��5������%o���o�&�}��4jKR�dg�Æ]4N�˕B#�l,(���:E�``Ր���]Q���X��	R��Z��6�K�o|o&�Y>αG=Ì0E�e3Ɛ������m_�,/�gl��)�,����28��(���a��RqJR춇�?VI ���7<�����[$�5J܆�)�l�8�\*���$X�-����9sl?��sd{��EA�I6�;��=���3��L� {�e�?[��M�R�^������j�lJ����R�mx�x$>���S�}�$ŝ�zw���"{���Ô��[Y_����L���"����,���>���ˡ�X�H(OI-m�.�y���|z���y�����P�G,�ʖ̍7��ת{�����ʱ��=��ǂS�#@Ȃ�tY���W��8A�l�v���9Z��T�#���AB�:ɘS��׷ qr�cln� ��
��Cݤ�f�*�\�S�}0ζ0�Z��S�W�t��'i��n�>�L�*��5��/ס�
$l٪L���l����5)tBy�Y���l%�	4T��P��6 BA=���J��<1<�t&�U�a���6�K�DU*����j���{��S�CrG�
����6s�<�h�?����^�'��¬�	̉v�D*��&w��6�0��IdwӢ�-!?%NPR���n�����)E�u6�Q��Eaf�E������E�����~z��)����ǳ�>��t,�d��H�%>�$�?ϓ��y���{�LYHǂ�^-��~Է�]g���.�縄0��P��Zd{������`pBC$?~���vƍ�a�'F�P+￥��-kvɃ]x��?O���2<tُ}:�BD�Ck��+���$P4Aw����$z�w�$����&��'�e["!�������������� 8�(+�	�G����"<
�.ƖΝky����ڰ�F}Y�8��w5S\��M���q(�8&��2<]{���s$�rk���>&��#4L�J�ό*.U��)�qWV�x��k�E�O��7k\9�
�4};.�F�pۜNS!ɋ��0ݚ�=��na�֨�()�8oq@<p������0��LDZdt�9��f�ʃC;o�\���L�`d��V�4���a�
�ɇxȜ\�u��������8m�V�r2�?Ff��ߑi�&7B,r������oݢȿ-L;�_�$fzd�����b�L��o�i�18j���Y��Z`(��F�Yor7GTVNp��0��������M~ғL�D��pMW�m�xf�˕6���*�H��^�t*�x�����@�e�>?"�������5��0������H�Z ��%�/�"����߈�T��+R	�2�%B?����h.=҂��^��64S���hZ����"��#��qj׎�8b�x��{ʌ�F/噱���4��_�Ɯ�ۖ;��R�d@��c��Wގ���J����é����v���!��Ր@��iΒW�ЕT�BC��`<I��5���>��T�g-s�d8���1��W���'��&Ȉ&VLnͤGAZ�6���r��$���x�zA���rz�;h-�����&Fh=��;Ӧ:�{�Eq�˷Z�`E`1��-�g�z���\E�/3�H�ʅ	|��2���i�?h�������{�;D�S���!���o�!}@P���4��`H~B�\�\�o���Ӵ��Ӟ�{���:�R��eq����ˬ�����V��mD�A���Q�Ѻ`�>���O]χ2Խ7������c' a�g-q\�sp�F&�D�����~������`)62Z~�
�y���QP�[����b��B%��RrM$���}�C�Q�C!�ہ+��&x�������TD���Q���z����Ӷ^d�ԗ�5�g HY��=�˾����<߶j��K��W�2���T�ݢv�O��۶�8�V���J�
s�-�!�J3�XQ�8�:ӱT���]Y+�ï���z�o�3�V9��ޚ~jZn�`�|J� 3����FB���/���r��"(��QN��6�h�g���j��Ȫm���lcv���ɚ�L��ݯl���q۱���3g��vg�Iv��r���t m���İ�S��t�);˗�mu�6vYsg�����t�i����}�YD�c&�)>����\�wWl e��ο6l4u��/��qF������x��([Q�����Z'Jkx&�����P���� 3<M�	T�����JNS(��@��9����d�>}�Ķg�!�O�zc)�E����9���C�y���\��<њr~����̀�\�Hx�R�J
��8{x�/�N��[�h�Muq��^E��T�+��b`�{����ױDM�-50���ӪU��y
�V:��������o{��?
Q�x^����ǚ3/:�Gd�����Ϲ����Q��翸1������.����%D�����Zꋉ&�v���L����g: �ƚ�k���>��f)%ou��D�C��<.ۛǫ�ٔ��laP�������5��v�����G��'�VnП�J(�G�!��?�{��K��y��m��C|�X{���@�u�\�2��
嬳+�S�3P������k�'�[M��xܫ���[v����?��0�h�/-�qy�gs�'X��2���WzW����E�_m/����b�R��*=8��6�X�>r٨/������2 �/>>�v��)��*n�@c%����0֋�w��kg���2��ms�V28J}S1��}c������al����"]�p�{����=�j���i]�1��ҕ�Zzm�c�}�EQW�-c�dgv�j$�K�끌��#;9���ùV.h��[���'�i�ݼ����Y�l��}��T�{��TII�#b3���|AӁ%�J�H�Û����Rpu��2Q��]�K-�����_���=�uy���F�,�U���E��w�>����Ԯ餲�p����;]�?��9U�l���ﳣ�VA0vCJ��}�������������9���g����F�����7 'E�@GU��������\�0�/W����?L�o�@;�z���K��z`�z�����o�ĕ��j�xvu�� �����
���Fq���E}�����2��~�rSc����Rϋ!p�@p]��G�;���v	��d�p���_���W��Ϛ�/���B8ʹĪ�Ͽ况G����bDo�������g+��g�@#rx"���}�<�8���ף$����ʑ��^Q���6�l�X�g��z����_�$ń��M%a�����n�#<L�������ȡ�Q��HKbe���o�M�+�,�X�ĵ�0���v�0�XZg�>��^ U�=[���*���k�%�`N;��WLǮ�)VoF�����B-�W��
��'`�^ �b����J��Ҳ���5 �i��5Y���AY�Z�~2y�&]���!���k��oҿ.����jD
����̄�3���$��_9Q���y��F.��4��b�#�~���V�:i|�ʣ#�5��(���zz�#�M�s����(�"��ž��<���Y�W�͎OW��(GX��T�ȭ!����jN���$�Ȅ!�7c�H���p񄅦W"������~!�<�vf�ȼ#�y����p`WpvT^�;X�r�x-�9�F�(ϒ-���������<s���?�)����ZT��D���B�s����%�Ҷ˱��%.��OPEK����7�x6�����-=uT��(����s����rX[���=Qg��H(y�Hcd>���j���f�'Ջ2�j�$f;"�u��Jp�\�)T,�1��ww{�h-�E^�y�8�>�:��X�3485@�@�~��#������
�cͺ=	$Hp	���h�	n���k���Npw�&84.�C�����3s2s2��/��꡾���k���Ꜣ]l���1�%65�!������:�i�*��tа�o��]�h6�(~
H*4��=M�0ru�կV��=��ʙ���f�Y����*؃C��Tz�:�+��
�4J�Q���������{)^}ϝ|O(�ɡQ(�5'�QH��Ri��qV��z��M2al�>E�{+o��F,�M������=��w�K	�uA�;硾��_�yb*}��X7��VS].]e�L#��Z94��`��+��u�cyw���Z�)$��MI�3���KG����O�ʹ�,��Á�����]L�z ��&�����q�]}�U�U���U[(o%�����6��u'3f��[��p-L�F��Uf/�-��K�4���K��w�
��.��?a>���͛�"̋`y|\�T�(C�]�D��r;��i�$���d�y0���%H��iݧ�؈�՜���5Tr�k=c&t��l��԰'֬���J�z;�r��.�ɰ�©����x��&��ۑ*���	l���ǯ)�0����t����*�>W�2�����v��}6������q�����٦V��[�o��4��ߖ%Q�̇�ǉ"���]�AOC^����$�߳��p���^(��8!�k�L�������č
�$^+��d5�K�D	f��%��Ƅ/iW���
�(�ݕ��@�7�>��t�D��ģ��L��F�,�\�ݱ�vDI����g,C편&{������k����kL��$������WuK�9V�P�����,E[�-��ꄄ�V�,6ɏAg@<&�XrZ��Ko9������-A�N�[	�b�o��=7�����9�-����i�[ϖ��������-,�=�>J��<�'^x!+ԙ��Qq��۫���+�B�BQ�h�*{�<��iA��N%M�{V��Y*��hL�^o�w0�ʒ(*]O�վO���|l�;��}��ǉ��	�k
zcB������@5@;����]ֻ����� BvK��4��l��*5��%�2:9���<��T6;���ۡ��z��C�'�%�Ft0�-����x�-���s�Z�� �Y{�H	,���ڟ����<!�Y��$&���Uu��8/�ה��e���䵺�+��ݟ
N�ܽ�1��v��������3�En[�h�
q{�f�`ZMU3o:L>�Z�>6�Q���|7�-����4��z6z���odh�*'h�������!�|t@HV��-t<����W��x����O�I�Wyŉ���HYSD�],�4��bS[�ػ-��`�����/ �c+@.A�u�H���7��X�9n��L���C1��^���,尘-�E3Tɞ�˿�g+��2=�;����-%)�VU��SepiWY��`Ha��&5ϵI�����r���ݤ�U�#۵�Yې�M�Г��R���dr�&?��A�)�j�u�'�-������O,���'�-��I76m��Ӭ��8�*�	W�S;���9��Vw�b�N{��b-�����	Rf|a:	��ר���e��)^= ���1|'�`7�+܅�kWp�p�^(˛u��3��Vh��ZbƢ���	��.dL��yM�ُ�& X��4�ĉB�ŀiyL�+��m)�C&��WzI��z~��xx��nuZæ�n�Z�}kG~=�=q��AK$�����n<��nړ���d�Ը�|�u?�$'+z��	Kյ;��
������U�%U�
s�!��}�k���i/|��B�+#H;��x��� ��H\�?�B�D�ޥ(�b���Kt5a��p{`��C�OK6��گWo�A���i ���~�_���5�Lr�ؽ�ҷ,n��+��j�ڃ�6��y��T]J_H�Z�йx�F+ld0��7��'ć)i��+[p�$o0��{�_�&��f\!�z͗����ę��D��O%��$Zb��@,���%򵢞��Yg���/��~&�R ��Y�ԔQGM='�����Vo�Jd>����f RaV'�N�(P�me1{x֥v���|5����w�=rϧ��/����%�BM���k'b���jWf!�/���[�vn���	��FU��1tp�@�Q��(��K���%�<>A�i|�sA-�W��'b�Fb��/򣯉�B^��F�iM�ϲ0KԻ�j7�E��ejzݵ�1U�߾f����G�?Iϝ���$���:����5�@8�O�F>=����T��I'E�� ��:�Wѐw�Z�H��X���1BC�����,*)�� )d8�R�[5u�W�|���3�J�,��eb���*��.�s�V(}"��@3D��6`����X��VY;��jF����Fʄ���%Wr?��K�,�;�K�W���1�&�m�).� ��	#z��6wr?E��;~�io�0_F�s��)z�W�$��
4\.�=vغ؆���A���j����t3z6�+�b�$yߣ���\���Ơ&��^�!�ˉ�-p���'n�8U�vb�멦���g�e�6՛��ðQ~ ⷧAH=�d[��ΧT�~d�O
� ]�~����)F�I��>?��poxa$�IMdqGTy#���W¢U8�wti�0
ã}6b�m���Kv�����[ŝ��z�=�6����,#���M�d�p5�������~>��B�ӷig���Mq�!���2���A�R��J/�LT5]H�4�sv|jP��Bf/A&k��uzEBf\�n�s�3d�2K�1�(��Y��O���K��� ɷ�J�}��]Cڔ��ׇ��o���4bU3�0w�<�a�Є*c�5��2T����__������g�LY��6*�k�|����o�D�u�-@������8lQ �Cj�LF�o�s�u�D�o}w%�kdӣc:�]Ro�[Z�z*�[H���A����kHB5�����P������m
��1t��x�g `=�<]I3J���@�}����'J�-�8&9�fū����7�;�Uf;����R3�=�7~.��2��[N�+���rX��U�"��C���W#%M�����ǩXw�c(;�+)FPtء��C�R��8b��eni[������D�u�F<�@b ƽ[����\l���#o�y�\�)���s�Ij�M���d�߸1�u(�_�8z��;�)j�WKә�I�Ϫ����b8��������q�D�oJ�r$U��H�g���\/m�{]r� [ص����E���c+E}�[��ԩ��f�kNYɤV���%D���"�1�*D�������k�lI�6�݃W�'=�����0X��ʵ?: ��A�'��Zk��b���&��P����B���Z��#� ��W�����8��V��#72��怎M�i�c=��d� n�\���$bʠ%'=B{�=H����Q[Z�C'DR�n����AJD�E����#�~!�ryWQńn��x���?�ˊ��~���?]@�Z?��7Ӳ���$��os2�����;d~rm�V�G����n/Z��Se������a:���c��>AsE�vP�����%I��m���3��ȳ_d��6M�^)~�A����~������V��f4�^��a�`U��b�m:I�ᷞg���_-�OR�3�.p?Ԅ� �P� u����裠�	w�Aβ#.�&{~5��
��8_w��x�]a�s��u�,o�N��b�������.[���,�����e{���J~1�pseS��Q{^Ma�Zw=�t2�s��2YÿG(�vM1�E����?b�tn&Sz��[�Alr1�璲$6�����~L~��)�ɚ�Y��>?R6ֳ���#!�l�b�þ��!��B?5���AB�R0b�&x���a�4q�U�XV�<���F�t��xNףU��"����A�7i��B��*S���g�t	��ڏ�7��<�]����(��N<7�"����Wp]�평��Ʋ%��D7J�����Z�Z�I�L����N{����	rrr!]ۦ!
Jvvv_���������/.��)�^ۋJ�<��W_4R�o..��|5E���$U��~,���u-�y������)5�c��g��{��}���= "�p�/�O��״o�^��٤c'���}�*-����P�� =|�oN�����;$X2���&�Aq�(R]���-���d�~Ҩv����<��b��O0r
���NR�Ur��e�d���ػ'b�u�_�|#�}P��f��2�	B9�������fn��vyT�+�I�ҍ
Y���d�� �X�
C߃��ϓ���=�XO�i0��+��ڽ\���|\�����F�28$��)�/��I���OdS���e0;C&���vG���ŲF1���>4��aT�K�px�Y�4��3��'1[��Am�P����N�m�}"n;�i�N䫆oM�π}�iRK�Z�@K�6� 5�M�|J��c꽞�B��T��Gm�mCyc �$�^�&i'��L�h2�{�K�&� ҿ��o�z���zuЎ� ��;R�d����]d>�T1�$��i6�2�}<!;�I�J.͵vh�8�'Bt�O��.g���c����(q�.,$(�����=�>b��?<\�UU�&̲��O5�����M���R�a�g��3�l�����s>����}�C)��Yn� 52ţ���J
���õw��v�p�Ur#���/��i3@#���5�jG�Ӟ�z��E]9�.wև73�l�^���*[����ҥ�t��E ��ܲ�����NՉ���h�}�ᮬ��x����fn �ue2�f�P ����Xݘ��� _n!�X��WzL�}���B��Wv�b9��=cn�3�;�
�ގS�uW���lq��-:�ߙ 9�]�OoM �E#�k�y�~i7���ӞV������q1W~�9��&�����z�-�3�7k8R�is����Ռ�%�
jܝ�6�3����ayö4�f	��J��%o��^گ s�7-ŵ!bk�K�n@J0��f?V�N��VZJ#�vj)����/P"��߹sa�\w�cA}M%�Z�۲����U�v�ga�vJ�����;!�6�m�oH�t�J�֜�p��N��F9��Y�6����h�fL��*@(��-�!������<�5�7������ؙb�r����'���|���tI�ن|&� ����,���3��6�Q�C�҈|����Q ������+V��&����W��ʱ������E�M�!��ooQ��kLΝ���ޣtq��BgtYSU�}��4^�¨���lMY��?E���xo
2���{_E���L�O1;����쵑��	窰3�R���w/{���ۀǛ����w��vi*�k�3-�F;Ȣ�'�G+�f� i���$���!�n=�� %7���]�Cn���vd-n�j��͢�Ȣ���s�ﶅ��v"���Pe�>)R�
�ߣ���{�y��=+,k��/+K��	��Cq��2���kX�{l�޽�R�ikz��Y�L���)�JT����_Ρ=��*�l�q�Y��VT��S��q ��ns�NծYO�^yq��r�֮XU�;&6��L{�	!b���&��5��[p��]0rqk�d_f�.�i�a��.,�;^I��X���z�g6V`��B�>#�OӁ�V��s!��7Ҙ�������N���Y�tM��%�����cS��f�L_Z���� v�M�ӲK}0�7[��j��8�L�`�9�|)����se�����J���߼��r4�����Xu�6	*-܏�sb�𶦓"-R����	*L�CP�b�U������rY�5�>���&�6��7{���A	�L���j���^��b�|�%��[����:��XD�3���aAy!w��
D�d��:5S���,e�ea�_�@����)`�hy��?����4��<���a[d�S2�9N�c+��* ���wٯ����W��ojN�ٜ�04��������vȹ~��kQɐ�Ʃ�+�lg�`�1I�R���S��֨�ZE퍻e2�Q�$2s�����bu$�|�,���ݐ<�­�
��f0M{��_��^2�BR���"�nh��0u�R�Щ٬o��q�p�� ����u�=3��JN��ezȦ�=��
�:���@���۷��&�S&�K�52���@��=���6ܞO%4�V���/?�S�
�{�C�v��r�v~��8t��ݯel��kj��[���U����7�U'Lr����|�ʓ��gyZ�Xf{�x�XV(��ħw�75�j�G�Z{Fj@~ֆw��OU��\i�'�ē0���	�ޝM10&�]���8TQ$�ICQw��7,to7)�U��\��[�M�$�^d	�-������T���2v,WϸWQ-6VJ�����K�Qq���'n��6�zk�g,� n7m�
qo�`����}s��h���{Vx]��#t?����ǳe��z`yh�$������g�.�dI�H6lR*�t��L�A��[�w�65�9Rr��<R�ل%�~K��9�{&�arJ�T@���������l�Z<�aì0����/AD;JՓ��D����n��=I���mFBn����K����G�$���b�z1������T����Z 0��-Gx�B3O9�C�z`to��գ�粗���5zP9]��8�$���qX�2 �9�٢{(ӱ*/i��#�)�؛&��A���!@�����[����u��zÙ��E]�!<�o�!tzHH��0��>*���F�&0��=[�Nr��e�b_�S����!Qb\�
9�EY�t�\�{s���4J���H��G�+��͞d��0�E�<T���.��&��8��Z���,�����ų�]5�`!��(*]s{z|�d �l��؏�����"���pZS�K���!s�(��1#�;9<	��L(J)y�m�]TX���馢3����r�H4�s �>_��[�X?歊���
K��ش^y�m6[8~�L�	l=t"4�X�R���vʧP�$�4B��L�L���7���҉b��.��6���Z�7!%���ʳ ^l׃�k0JKV� +E=�3��2pʇMc��#���s�}]
��{�Eҏy�`m��T�8�%s#s��ߜ�-�̗*	.��N�����
�������ں/
@1]�'���#�'��G����5� %��b�Z�_;j�;B�K�@����ٗn�I�Z��ϵ��������޺�NdM��<�������wq�O������=?��^p"�a���f?"%-�Q������������s����M@���gk�qѭ��A*�~��x��T�?\�}��Im�V�-8}e߆W�Ȼs��fvHK�k�/�x��σ����Cл�TdՈ��q���jݟT����
��B�GG�;gx�wA�ߒ"��˶��� ��u縃���3����E�~�,�ahh���Ȃ��3��rh����x�I���r�m����RN��w��b�
6FG���������Q�]�u�{���w��*�7��L�l��׶��J��Yȏ�[��`��m*~Y�3W��s�22������-Ԝ=����$��dQ"��x��:�^)}�XR����hʏ�C� ��w��&1=�P,R5Ճ�L],�&����
W�+K
�-��AB�e
my-]Q`8�HO��:��Z�ز?(92�?��:���vd��Ƙ�g�m��/C�5FGTgi��aǱW�M[-�`�*�۵�w7�[�2�j�2@j���z܆�d)w�7��ܐ�%ig��
�&��-n�-ҚY˜�����#�f��v٧)��&k�h����y���y�ݺ�[/6��D�m�/c�\^���о���b�ڴ=����6�cKe�v��I�h�-���Y ;{zZ��������7-֐��$$��iu���tQ��hn����Hgw�7�����^c-�{�sU��p��UcP�L�R��G�B������Ϩ�=��j2g�*�$�#�T�K��(��_�ꩌA����2Q�߈��3�e��)Թ;�{��=E-��,)j`���C1��g�#>�KJf�KF!"��S��y|5d��T���~{~K�OLQPZ�A?�����I�u��@��GAM>�Ob�E)�,��a�s�"��5��"i)y�7� *�8���d�� �%�G�4ڮ*�~��Q�GIpRkr�讒�m�F�kH����[���%	R����J��w��W{jZc9^}�9گlc޳�����R���_����)U���-aT�E��)�7vH�/C����d�������x�$������THNE8Ϩ\x �0�H��d��kMX���ss����)d��b�g,;�OOD���\��'���V��v$��$I��e�xy�ߐO�����/�����A�c�~dm:��3�m�����~uN���]�?I|������,&+�#IJ,E��!> 8&�������x��\u,Yr\q�io�/T����;���%�M���5�����79e/T���FB�Y:[�j0����T�MR���2e����+�xS�i1���Ôީ���Q���[!>�Z{^U�/�Y�
8ã%~?z#w�b��K�;X�6`�\
Z�����:�o�\��-	��X�`Z���{{�C��y��kŗ�/Q�)�ߞ��M<�O��bz� X�'W��f�u�n�D�y�+��}4��n�oe:�*�k��p m?��8�ߚHG���C8��|H�G���𨀮.7�q'""+���]W���9!����n�b����<�,7�O��h3&0@q�F8�_z3����a�����iR��ep����;V/�`��pd�>�򟵛k�_^�OW�(g����8�3�%0:T;��r����i[�1�Y��Q
���ӥ�V	(V�������|ѕf� >�W��J����@��tt�l��ݵ�#)Ϻ�������zO%�.1IE����31��n앹b��7��1�<N��5<��W!G�3R2�x�-��#N����2���{\#�-X���#;�1�P;"bA�ݴh'ß���1�F�aҪЪ��OS��b	3<
�N$T�[rA�4l��&*���W�3���8�ht�ϧ�i$W���f��}�h�5����b���P��<��f+�CE��z�J�¦�6���D��OGxR���
^s!��cc���a���	�By6 �ȷ����G��k��L4c_�2jY��GX��9S���� Zk+~7�o}<��vx�'*�+�!�j�
C<��U��ξ�y�ϭ�:���(}�ޠ����~�-�2g����� ��8��}0�aȂ��T��K�Ӏ������$&�y$������_�󚻍��$�������$���?'*����l]8>>>1����1��YM�wP�_��м�p�ܘk��G+����:�Cl��Í�nJ��/'�%A ��§���o��h�Hk�<v��y�FB.P��c��aÓ4�L���ֿd'���t#E�?��5��/������'���^4]����hq�6�?����h%��lzPR�x���=��ZC�7tHRO����V^~�5O�T�Nָ���`�!�n�lU��!����!����Uh���sw��.�����C3e?�ߓN|ۏD2F�t��צ4a��UKU����(~���2Wlgk�ם:./x�i��ܸK��Y$BW���Hm*�hU������ߓu�D��)�񊭃��X����9M% BӦ��dɫM	�R��X�$���fe%M_.���C7�0��V��C�v����Ļi/�l�lFc`5�i
�TwO(�d�y�re舽Xso���	�G�<�"1>1���u&�Qz�U���w+B�4�Z<�v����x%��X �Y*v $$d0�K%krT���f���dVn��x�36rk�47���<n0j�D�_������À5��2w�s�hSI�%W�E=�]8ۮ����2�X��Ş��	��/�dV-U�/���";�w��r)�Cge˿�ŵ����9њ���l��F�9	Wҵ�x��N���y��
���j��!D���(,�� c7������Yv��a��e)� ��%r	�$�D�jN����^��c�U�5y���G,��\O�Tt��T�C� '��ꏤe�D�&��kk��U��Z.Ne�̐�����/6��{�T	�Y3�hte�n�A���S��Z�����o��T=(>���Cc���%)=���<���<�1P��=~��i��&����B���x啗ܶ"iT���t����@�����ѮGZ���*ҿp�����u��`��?8u�����ՏZ�QA��N ���ǌ�嵾��{���My��?>��r"�Bz>�PK�}�Uk  �t  PK  o��U               word/media/image8.png��eTݷ�@pn�[p�wo�wh$	�'�t��4wwww����{�}����8�|��CU�Us��jΧ�~)+J�} ����+4iq�W�^��H��l�ˠ�z��YF���g���;��[������ؔ(�rB���LL=<f]���-��$�����_��P�.��}���/E�荴�{?�@{��y�noÛ3��vH�?f�V�h��Ks;����H��NO�᛫�-Q��	�4��=��ㆰ�U�gb���w���L߽�[�Zun�Xt58�]�L)�/r�#�o��E�Z�����ã�啂ַ%Ч���=�z�!2Z�E("�}Ÿ(~@���#�%q���`�:��w�Wk���:��/�1�ϼp��+*��X��Ng�H���Ns�A�<�2Հ��8�n\L�eA��(U�]�Ҧ��m��t���ύ��%�6���.�
S��&�S�u�CZ
�ؖ��H~�X4����
I`Q𴄺Z�k����6< S���G������^Y�<��?ͳ�ۊ�@�.q�پ��z��w?�W��{6��wO�O�u�b�t"%M!��s{<�@iJ�����$�����ѽ�\2!������O6���{D��u��1��[���)a�U=7{"��b����cxy	�[�����l�
���u�&R�cWz
U���JFq�.5�4�zs(��:�U8�Q�dI����蔍�qy�\��h�*�NA5�2`~vG���N�D}ΜPE;N��n�V$��m�MDF^ �R�7�͘0^�����V�_,�e��W�>�@�p��q�wp�x�rw0A�+�ò�╋����pj��Qb�������J荅Y�K�Dt���@R���	��k{ |��8 ��RjUyjW� ��&��d}��ou� g~Z�ï�RwZ.$zn����t��ܽ�7$�ȍ�DCG��_�Z�����5?����6�28[��*qe朗Δ�/~ӎ�����g�dW�u���������QD�I0n�֗N����6?8���qww���%	����?�=�bS���ll��6;�Ep����s��E�`�k�l�ű�����"WL���e�����)S�Bz��YM���)L��S��o����^�όu��Ɔ�p��*M�d�B�&�:]���=]��3����=�!�^u�jP�/Y�t���*������e�+F�s��	@�5��i	�d������eU|�/&�ҝ>Q�w���V~�+t��G~/����c���(���D��z_׌��������9��g�srr2/&��)�,�jQء ��Q]���_��1c��-��@�{i�n�Y����A[&���,�y�	$���x�>���$:�=
}��z��V������רv?"=XR��e��+��-�|�I�7��6�)�VSoK7fCT]�'���E�4��`��h��$����}��{��/h�l�:_�iIjf�.�_i<[J�мl�+��
��nZ�<#Q�M��+j~�99�8�١P�l]�Ԉ� ��-F�A�=S����t��f<8�����1m_,�Yz����u ��ޣ4Gn|EJ�r7��i3���A�nՠ��7����$������b�̾�
���b��빑�����yh�K���r��k^�?O�ou`d+sv=Y���gҊ��٩���@?�&F����;$�>_<���vg�ɀբ7��S{��wp��G�M�q�D,����S�h���o���j�@w�C2��J��!
y[��0;�{�/G!�d'��+=AE��Q�'�|���=i��ԡc�xG��p~����e�v���ڎ���"1OH�b7|H^�,o�U�-�Y��@0+��3����6������W�1�/�l�W���Z�w^�u&8�Q���#��0x�w���h^AvKB�j=���-�@�Cq���w�B4��U�����Όz�~M�{�^�@+g�ϧbp>����rU�9������{>W]d�H�6b��73�ip��������"�D��~�=�R�%�-���j�n�)VSb��e����3����s�h).I~�3�@M�=ŒH]j��S?�X	Y�\�����x)�:�Њ��{�Y�Nh���C�c_ ���� ��N�RiwC�����1�ʠ�� jYt1���bwLl�SNη��#���|� 1i��,`��&4���m��Zo�1#�X:~�G�X:��pa�g8_[��0�TJ�r���ۂ��MB{����̓?_��F�4���O0 ~@�H�{u����s�����uȅg��^r�sʾ�9�t�r�����'~�Й���T0 ��1�R#B��<WJ6����7�)ZF�
q�?��S�x:��(_S@1B�F"�c0Im	FԆ�A�x�7��*�����{T���O��
j����Vd2��X&F
7���H�K� �����#�=��|�E&��`�AF�	[����:�*-��Ѻ=Ҧ�[CU�+���8��ɴ��Q�~�I�kq`+����'fB��N��S�a/�e�J������塴�^�����ŏ%ID�p�++o�/��_L��DB�.�<���7=_�*9h�@z��ar���қ�VO�Ï����:Q�p�N?K�q�ș*y�1Ј�!k��ޕu{ Y������}� 4d��ݏѢNx����lb�9!8E�]��1�Ւ�k��6.yh;'ǻ��1o��F�x�^�M��O�����׊-�Y����~��M���)�-�!g'Fdpv6����,����LqF�d*$"gMP���X��[$(D�"	vf���|a�/��!j-�'r��5���AG��Б��+��<��A����lsZeًLMY�X���Qpē���8�Vd)���SDѮ���b�8��\З{.�Z\�f�T�O3ml�}!��|܄��h�e��w@j�/p�+UG���B4Q�=��Dy��a t�B�����Kt��ivp-��t�R���fMg.�h|}4�f!~[<�V7J�*�^I<G5�L'�u��Y�J݄�Np�߰DϳCyP�^}*���Jǎ��q�?�
��+��ݹ!���5C�3��R��o�i~��ݚ�sl�odHN��5T�/(��/BtWs�Ч�2Uo���c���*	��TW)n��ͥ��G�n��L|c�}j06W�[zohB�0�%s�|f�$�e�z�!�	ra��t���C�e՝�2��s��Msw���o��c.P'�d�<���FO;�!K��UeDQ��bU �₭ޞ�4��9Yh�$�˚!'=݉�P�N�NO�b��v�V�m�N����*x��T�
]���d��<�8���nC^�o���GBo�D��N��T�8p$J��4*�j�n݅���>ғ�̴����lQձJ-��8xE��n�WNvD���pT[��a�o��'�Q@^:�߹�������uݟ��-��@i%�f�U�Kcu��ONr��C�]��/��m������\XO�=wҨ�ym�O7d=�-�?�e���x��:΁ w�lJV��5�L�$}0fc{l(ܷ©`�f�;o����j�tΪ_`��l�5?׫~�@o�o�YJǾ���l󽪼����A��8������~:�?L�4�D��g�k��v�l�����M�����I�ȡ���]�!���V�o=�]8ދ�m��U汱�aQ����i�̀g��w��A�X�ٚI.�!�~A��.,~W'^��Y�21��6<�~�V}�����[�r��mN;����n|�ŷ����:W��������-��m� ��?KL�lZ]���Q�?��(+�|����c�$�q$�����4/�<A��P������7���@��O�_�K�Ls��C����.�A[L���Z��<�n��e�7�b��c0<�O�T^��}��3eeR�'��\>�8�Й&Q9gI������||3����6��'�ڢ�\t��T�O�%l[�?�vs�|�Ӿs�p�y�7ȴ��x���+�~^��|����՜k��p���� x�r�榺����I3�'�Í�1�����_̡�p�LqG�mP�Ip�\ޅX{S{�,����.��Z��
����mu�lVFC_KH���)���k<�����[�S��)x\*�;�Ϛ�^��.-VG�P�'�4��"@���Xn9�
'�\���;�v-��9L�=�wi��q���=�J5���y�?�6U(�@
:Q.r���U�s{3�[��^��zK�|�>;�>�C��䡎E�ºrܡ�ңq����)AVnN_�C��9Pn`W��Dz�.�p��l�rn51Ax���Xvta�,C��ENgNP���@/����*X��(�YX+�{a�3A��۽����@o�{#\9��?�X	!:��4:o������גv핛֨o�ё�l�-A�$+���)ҵ�h��Ѝ�KZAa�FaO����X�N�!��I��G9|�x�C�/-�//,�}MiKK��p�8������'B]�x�a�.�X4t��dj�YR�y��Q��P�ȉ����k}��s�.����a3=�2�H�pm��J�)U���)���L�j�������衯��FG���fϞ�/��?O��m��;~���ip�lf
 {P���Ee�^����m�0%�MͲ�k+;���ݯ<���k���\.p���9?M���F�d	����B#��|g|s�nf(�@��_�(b^-b�<��Y�H����
�E�wb�%�.���b�������78� !4�~7_���sp�1�*g�$"J�6d���H�v�s����g{��;,�ۂa5^�Y���/۷ԇ�.J���t94�'$S�L����`#�|�"��}�n�g��j�S�C�+H�����6{|`e�Ҥ��Y�m��|�~���Jkg|{���i�~�n��}(gѱ�$���-���?-F�aR��=�$�K�-��e�]+����_����XtC�,�U>uظز�S��7�X��-�ɺw��k=��5������U���I�$����*׮ڧK*O�ɆC��$��vi���)3���?��z�?ޚ�Ŝ�!\j�A���%+eC/N�x��g�:��l����ɓ���ed���/��]͛����h'B���I��O���_�-�ꦏN����4���g�N�dXY�]3lĊ�c�GpU�}���)��ޖ���ѝIu���h�?{q����GCI'$j�BX�_�զ�͆���eu*����������)�S��^3�2I��'a�O���qQ�Y��E[+�%u�2]�`��{'����׳"�O��\5��-�
VdVb{�{�6I����Nn�׹�Krna��{������6UQ[La��e>��8�������d���qXդy�[|5.��=��Mʲ�����^��8(��(ߵu�0�h>��˔�~6�X��[�?�T�ȋQ�v����6lL@��v��¥�w��Q�Xz��{7Y�cJo��w!�x	l���n��3�;'�A�d0�ift� u�PW���TQ�W4c�0ѭf���M����l��¯���5�kI)�Ǉ�U5��ɵ�r��"r�r�/����m͍��R��*��]�j���@���9*���~{<%W����Ev�����.�Ȋ� PaʉP�cO���<��ޫ� =��p�MH��=~ ���k�@!l�q#��s�^�)��.�M���u�xZuA5%��Y�9�o>�2��z	oT:ooe-"AÇb����$~���D�]��(�k����0�@�L�adA㫫�D!L�����S�u��E2G�?�a��z`_-�x>_���~����Ug5hIN��{q�g��h��D-�~���J�w� a�Ր@(�h׆/�4@�8[F����wX�g���3bJ~������`���-4:��%K�(�.�3D5�<[�0RA�g�`�!!"�c����#xr0]����B�H��Y��B��S��xgd��Hu�%ޔ�>�p�����+#�b�N}�`��Q���3��&���K>A��u��R\~�|��?#)n�_��1d�ß���O�!!��ㆈ��N��l����AHR%�A�*g��@��jf��K�Y��BfcmQ�026V�DP��+➑�S�\:�GOn��*[/y�o���=7W�F�,C��M8����$�J�`�h�G�+�ٞϜ$����:y�3?,��V��?Lٻ��Q+�Ea��|�g",�v��R?&v�0�%�,=�h�K1yn��T�ӻ�Bbm�f^��{7밦wF��jά�
ެ069��t}�}�u	dJC\�]��[ֿy�L�V)gIc�P����v���y�F��7]��g��ہ�]��g�z��q�N�!4b�\�B�J<A�͍#�D��
/�q��b~�-��'}?��Q?��1��E}1�C-�A}'ٵ�.�v����N�gv���}�ߩ��N$���;��.��2D�T�21���IZC�F|�w�>i�輓ߔ+���f�ho8P�~{dQ�rP�r���e�$��橚��?���`Q#�`�~��0�58�*�+�::����S�ȝ�󜫦�(A,-��t�u=B�"(e�CAj{�����s�(�_�Wz�Eա z���(7�\*�u���Q�<p5����F�^~��M��E�`g0�8(�(�W�\�:x�`3��Baq�.o��+��b b��'��z�����Ldm��[:���[��m͍�p�R��lm�\�?&�T�;[�r{[��F'q�[��}�:n�i���{��&���p�����XM]��d�U��C\1f�|!��7Jym���?8��+	�t�'Z|�e�I$�C���-&��b's���V�j�8ҵ3�~��qT�V�Svv]_%H��gvd�=^�.�Ŋ��t�6�0$��������bp����r�"H�ڨ���yq�����Ax@Eq��F����Yj[>|���R���B���,.J��/V�B�f�X�9��#ȃ0�C'(}���ѳ�f�I��r�0Z�Z~r)�|�6�����J>�ʀi�"YGa��v9�5}m��Զ��O��<��n�q���H��݊�;\�6$�b5w�Gť��b��78�x}r⛺vidj��~�"j��IF�S����9�S��V�+��ߟۧ)*�(�ql�!\��Kl��<&�P9�P]ҼK��#3�g�;H����+����)��hLri,�9r_S�߬#����Ҋ��!�Iҩ�r˧vi�8��l�����d������\rXJD=M��4�s��/���޻
�(�82ޔ3ʡ��4�6&����g��.U `?�:��ѣ��Bb�
;N�������7,�+v�����d��)��
gN��Liu%gM����m6J1��&���G�'>�q�>�w%h�?�#����<���^�T���"8�}:�c]Κ�i��]͵\ݲz^�h|Ѭ8���q0���'��'�E$8���<�wz�Χ�y2�'��],�ִ�l#�Q)�Ph*X��ӣݹ�un��e=��|86��<���b��RS)4���	���Ԏ.�B��Q$�Ձ)��"|w4�`���.<�t��Fѳ�ƳŘ/�uZk����BB=�u��.S�Ĵ@/h٬�٪�"d������J)Q�~��hYqʎf|~<����h�)���a6��Һ�(�7#V�]e+7�M�VV�&�t���K?pj.o$��.�'�����Ht[�vϴ6 ��D����y�K9*W��,	��8�&"O��Z	��y�w1뷓�FSR��?AJZq����u���tbOR��Q��MjV��!�3)}���%�c����͑'���Ke,̧�5�]��ĝ�ޔs���d�� 
g1�ط�LP��`����悢2'_������V�7�W�����o��z�o��~"n���{�e�P�X*�n�$ع��X�K����Lwx/k�$�G�,���uL��LW���>�N�׸�g�G���r�-��T����:-����0���&bBI����k����57?��1�`vF�1MC��p���3������ا�u�&�}T���nt:}3!�D�sw�W��Q@ �I�p�i�����S>(��� G�+>�n%�v��`˶:�ю2�d�.�ю�k�b��.X�0t�#U���$�EW����(�_�#��:�)�@�%S�Q�/��2�e}?AZ �G&C!�|O�rK�����!������j���ΰ�%ҹJ\g�ju����b�]!�,0]�bI�7U�/�Ĩ�����Qj�"D���L�����<�ɱ#l����f�"�4w֧�2V�m�>v�g�jzhL�S���ç��(yC(f>Mə�+������'~q%���_x2exS;̴��P�s��X6h_�kQI��d�����E��w���};�B���j!�݈���L���aӪ�)rT�PX�sx�ʚ�h*U:z�����a/ܼFq�:j��`�*� ��˓����O�h���N(�'�+���� `cc�K��hlȭ��8�ʕ��;hJ��~H_/�3����[W�ye�=���X����R]���őǥ"�~�xi���&w�|0�ߵ��W;�Rޗ���Y=�V�
��ue�C�݆���vOn��?vl�����eE�GѳzCw�h]��z��>2�Όy,koQo�������355{F�d����ĞR��{vl\��9�^ͬ�Ln���S���>�th,Òl�^�>[D� 1 ȅC�\Z�px�Z���W�6��{d���#MŰ����N��=i��Fe9cŨ�O�HKU��ku^Wf���9�NOߏ�gf�*��ӥu(��:0T*�,�_A�]Gpg.��S��ӝM���ӾZ ������ {����7W�H���1��(�&N��`�Fұ����_+~���fSo_,�۹��*���p�ʒ��Ѧr��[3��Ֆ�8��llO�o���wb����o���t҂Uښ1�p5&�u�Ͻ/�ydK��a�)�Fe��T�c�΢��AAB��U�xM����+k?�Wǰ�_��(:�(�
����lE��#����^�F5�';_4�D:�+A3���s"��&`keS�m܉��%0I�_L[� ���	i�^�k\-�����>PD��4e���z�J8⍈ú\I��c�����y��P�):
v�18�5�=�X�&Z(˔y<������v�|��|m
q������|w��R��Z���Y���׹� 8��%f��ï���{���������r�P˝��eB���e������}� h**�P�Ӟ����I�#�^��W�����٭�-�=9=���\g@�lQ�Ul��p߲;-Q�֩�#��f��U�R�}�r#X�-���E����C1�܅�*"��ΝMM�;J�REX��F���W״��w(UMn��II\�:UtM֌N�B��zM�DՄ���9(h 4E����~4��LƯ��R>t	D2�!����8Ϝ����A4p6^�i��槃�>����ˬea�K9��cODz���.A٦��g� �a��~���I��=)��0%V%
�c��N�{+���羪|re�=i���V!0m�h��q߻%-b{F���P3��=���+^���"h��3S����1*ÖP?Z��b���,�0߳ԨM�<�]Wſ�-���䨦���б��9�FnK{��,2xG�O3��sj1���p
5�.&��{�꫸�1�j�^�.�เ�;]�#衛�	n��>��^�|��P&����8��Ob���`x�)�0�g`�⧝�`�/N3�q��`//�Z��)�A��Ѫ�o�dB�͏'�������ŷ�jO�;��2䫰s�̦���v`��)���]��>��D*�&��@�r(�V�bY�-��A����4�n��f��By
T�F��xv��,����6j�;�L>_�X�Z�� ������w�|��R+w��/���αG��X�S�����nW�kڑR�m:�U������ΟVAF�1��3hT��$�zƚ���36ۛ2��s�sQ��}�+7i������Y,�D��ɟc)�m��[�6�56��T����0�"4M�8mk������=��hb����xO�����1/B@�F�����S�-��f�ϓ�m}Ԓ��T/���%��}��)�u Uq�_g<8@�A5���%�}�
�:4�G��>�O�,���2ݓN�Lp[���ߞװ��Dp���d����z�/_�9@���e��=�5��F�����`Ө��uo��,�K��,��H��97[���lG���2�ږ"1�P�� ��r�*08O�}�_C��;=���B��N3{��X�$��֜$�Ñ�K������͒g|T������{�ܟ��X�Ѳ�/�� hfz�j���,�%p8�_̯��Q[���K�!W=����;e�/��-����FgV��R�7�js=��@n�i�:����ֽ�f�UY	�Qt&}��c6�����F
Q?�I�!/x���ޕ�lQ�P4�l�`����t�A���D���H���הz�}Tԩ���[�L:s'ˍ�^��7���̬i��K��>O	,�T�����c��V���E]u�B�"s�:s_>D�(��J`
i���[ODC?RPjŻ���T��"+������_5�y霤���R6
Ɖ�n]��O�D-ԣ���2�������S���i�&e���[��g��p���w�X�	L/C������w���P�j^��&w&b $
������8c:��1Tׯh����C/S&���Ŵ=�F���x�h�ѸAL�[�Ч��<��q��>e����Us�N�4|H�vsV�;�}������n.��tr�T:_p%�����cYy��JfDNޯKj��օ�Z���� @��v�����Z7Te�;>�Ce�$\�}��8�"�_�ps�r�N��t��KW�{+��������S��V]��qbU�1AQ�o��"c-�3��dHm���Ö�̶����RB*L^��0"�Le[�7T�����byH5�4n	�f"���LV�F�y$��=��#N �1=t��֌���6�@��G��Ҫ��m�A"�2�������ݢ2�#R6�g�y��3H����V��i��!��F��!5?*�lZ�l8}��?i��#�۽0��y�r䉏@E#�l�5�Z�֡���a~���"���1��^(z�@*���rG4�|��0&���Q�������}�j�>2;�J_#��٘ͬ7�6��c?���r���K��^w[�H$��.%���M*g:9q�.����}��ɷ���0���`��#Cֱg��ӯ�h��n�&IE!/�����╹���}f#�v�����:��Nb{Ӄ	ӌ���(K�-/k�
Ͷ���S��os$Ei��|m6T'��U�E�����&J��%�xP�ـ&
�a���	5l75_ѕ��^�,φ��;��	o�_*��k'=!.Y�0BT�:1�S:9���#�r��0v�;�*���ʓ+�ޔ��?¶�v�gn|���f�CSK+_bfV�J�\m
��o���iL8����WOh�Y	� с��!��2�	��6�@G�{ѪҞ�r�{�����Gv�<gؽ����Ʒ��D�I� �u4��ZKQ�K
�:��
%��6L���~���5���_B�9�r���*˼Z zX�QW����$�휐7�X�G�H���.Ä�[n�D��i��m�i%tH�?5j ��\q�/T��*U��E��A>6n�H��_�=9��}�l�zAl����8�� ���e*��:��z�7�]8K����o���'+�Rnv��c��_��vrf��J�()VJ��dC�s�4M���D���QP U����;�����1����>���.�@��S������ws�D��K�e5F_��3j⺧a;;�*��ƒ�=N�2�a���9�g��O[�eY$&���J��A�k����7��P��D���
��u�I�ǫ��刴�$�#XЉ����AM����8���݇��R�2��s�(�M+f-1X7���	���]��p�T�H�\���`��Dv�7��Vn���;����hDۺ�}nsz+��*�:2UZ]�R���z`��~.�7��Erku����~p�u_*��
���N㊝K��D�Y�T�����B��5/��Z�(�fꭹ�I��<� �f�d��py K�10�L-۸�C�B�ŕ��_�*@�r %]�=�e�P�Jo+K+SH�.A�L"��b毾�X~��D%eA<2�=m\򥀫�c�J�-PQ�<��Q��t�ة�V�-�G��)O�a�h������1�
��D�)M�s ~\ҭ����n�A�Z��B�f�7
����8�*�˂5�7#��Ƥ�O#3�f������牄��I���r��j�?�6X�h�%��μ����N��x�U�N��v.D
�x*u���ϯB(���vN���bO�3�����_�~J�ZBv��~�.?�]���G��Χ��@F`^d�X��]ӄg��%�I�"^���if���w�\F���t\��y����?�HFx��T^�^���rm��#�r����ȍ�HC�f���nƑu�Ԥ�]̝�{��`w�n�`�\yMp:��PT&7��;����̑�,�킮�H�Ig^�7Ts^�n���a�bp��7w|�4��73*xP�62Q�:F��V��c��2�X���>�7���W���*I߫̒K㼧�J�_k��<Ur�u̟8���3E`�X�>@^�L�k��Y�����k��j"�C�}�ҮX�t�]�NL2D]O�/y��T&s��pJFM�|}Kߓ���[j���IR�@<�+Z�P$X;�ƅ��O(��Ň�K����aq�|�u��*i�<ʾ�D��PϘ�Z}=y8*���\�?K$g�7�ޓlN2�ȵ+{�T�H�F�*h	���10)Ҥz{�T1������L�T���oRwlf������-�pT����U�P�\3��j��ZCS�e���F��Z��H k�D�+�;T� �kYA�A����i-�0�t!�Z�"� ��B�I+u��[���|���@��ڪ�7"S��<�S�. ��b '�Y���TW��η�ޓ��yN�����A����Sih�ލi[�`�E���3?ܔ$^>��&l����F�x�D��O��?6W�
&�m洞�ʜ��"<����v{�����$����*�.³:�Nŝg8]�����MK�[w��]`�P�]*k�/�HA���������L��������^uL�7!�����B�p8'p�	Nx���u=8 z�E:��֠�+��ߍ���+����[4��(�� �J��I�OL@�2$�l峺�~���%R��b=2��I�?X��iοc���;39:y��AH�UT� ,�n����U�n�;�X���|�14�����g`H��)Fƻ��M�ɼ���' ��j���׎�5�IX�.�V2���y4�y'�N�N7���%'\��� �KF��p�L�Ż�?vo�3�͐�i��涚B��Ji����
&\	�C}{�-�%,���3��xN^�Ǯ��&��*�����Ld]Q1��k��o�K����xD�K����Ψj�����VD(��}�U*5�#���?r��m�},�֨H�3����kh&g۩6�#e$�I��}�>h����â�������ǭCG�!��>-W��V6�:��l��j�Fe��O7�RĹL�&פ�7hMk� �\�k#�E�J~�4���~w(��<=dv�ci�{��X
d��fɰ֚�(UW�}�W� ��	���*: +1}Pe�>Δ�1~���:v8f�y�͎�AG�=�D�j��*9�̠��X���C&����/h5�c��V��il�*{1�C�C����QC�Ƞ����l�[<�Z	�]ș�;n�м���T� =���`�0BO.�����7��C~|Bi~��QҤP{����n�A��2)��d<L�Fb�:�$���.�e��ݿƍ�U�4�e�_X2_�$��(ϫ�*��iPH�����-������y�>��l�U��p���^�ǝ�3����0cd�,6�	P�����������~���/�S�s7�T<����{�_a �4��uV��9,�P�=G����	�ݹ�O�	��R�L�V��ٗ���5��~�������O�E�FoYQU�'�kRƿǢ��"�夫�g�1E��+�.i�H��V{܏�y�/X㵦IC�J��6��bxD}h�����w2qh==��h�nQ�8cu|u�E9�g����I���/[`g���F��Xό�f��rv*Y�A�]|����ѻ�{��|���|��z�k,H��|ar�	�e(^�-�k�/��Kv6�����E�ǘ�qDm@�����h��U�j��.���v߾e��-��ER�'3��呉x|M]l�0t�+ �q�P���z;~n+� k�4��=xZ�7�>3�av�*�pO$B�2�J�?]�^c4��Ws�"oq�j֧U�]��^t�����O.{O�N1���W�$�Z
��c�II�0j��7Y&�[%�Π�w��'����9��d�%����Y�^��!w��$��)W��1X�0fl�l�1(#"s����J�f�}=(��m'��w����Ŕ�
���
�n<�f6%�W��fL���\���:?�Ĳܣ�?ȶ�����E`k�w�P`}?�� ���^k9���,�'����uS���(����n��5�^US��_-�3���>�AN�� �kքv~�>S���6F�U��և�;Լ>��]��s����/���^��.�.��r���W��F5a*��:� Yx5�g��!)k��������q����X_̇_���	��S�_��d8���~���3�R�G�y,���]1���l����� g�Š�f��b�Ɨ���'��1�;�_T������J�%���cAf 4���dYF�-���������-���l�PN��	� �*��Ǘq�W�l�&~��X��7��m�3�e�lI�
�8�te4�Ί$�`h����Ef ��Ƽ�x)�J�=��i9��N.�=�'/i9%�.n��_AHi���!z�g��>�='G��w�ढ��)��S����8t�\����R������2;h�,v��5���$Ϥ�Mr;?���-r���y\"a���a���蓽�L�DZ�-���G�������}7�V�����p����������a�.���(zDQSR�K3�[����WЎ������ܙ�&Q}E�����JT�0��~��'A��� Z1P�D�O6yS��E�/ezYE�(��k>~\�+T���y@�J^�B�Ħ��f��`��t:��M�o�
�КHJ�kjq���R�ߏ����G�XU�yl�u�r�n���I�O���%|�M�G��*Tij0X����+H�<2��N�|`^ۥO�3�T��)N�/F�����N�jkj��f��s}<�J
R2jr:������רf	JÈ�ii��_�tȔ�� 	�eW�B}��.g�<\W�{�-��sa]q���ەϦ������'�_i&��c��>���R�C��"�|hn��@%N�]hl��5I<�WO%��%ݯ��b�aa���{u9�M��F���:���)q$k�����W��f�~މ��j'��+>���_�/��Xq���1׹@'��>$,��_��V}��0��@l����Ld��x����K�D��/��"�D�;�{�=®�<��n�#GB��ղ�21<��]�A��bn��w;�$��(v��S�Zs�����٠2��}4��K4R�Ե|0N���R��J��s��d5G�����6��-���k��i�}�و%;|��ui�J}��z%P�|@!ut.Cw���hT%�3G�z����Kv����e�������iz�P_� X�JV���G��S1P����i��ڒ1�O��vlk�^l�V'���7�}Է*�qX��ߞ��>��n�'ɤ�U�c��0��˴zV����j�x�w�K�H�JN�q������p���s"T��j��ye�mخX��>"���:ڋ�-aT�7����/na`���g3`��U/����#Dut)C��?%���wj�[���x��C6Q)?^�3�e(�b�1DU°=���O
�e�)gY�<[�<S�6����N��B��kZ^��&��A<���|�X@��(s
g�("�:�=�9�j�&H��F�����n��2.Ȱ/}q7�\g͇��s��G��wWF��_����XN�~�F7���M	���%|�?d�]��֒�LY�WuoW��w:Bp�K����w+
w)�݉ ��p^��ݩ��Vh�I�LOz&��|��;\�+�U쵟��e��K���x^�6���	\�ngeu���Rw"����LS,�\�4���`0=�������-��"`pɘA�;c�[Y�v�����8E�2��b(p>q#`!nx��v	M8��-Jr�BcY+׋[�֋2�3�=c���T2;�Ly�EB���"<�q;�f\�F��@��C�������h�mE�̂Dw�z���|�E�l	hP!a�[j~���nV���~�����7��qj����c�MU�<��8#w�+�|���eì�KS.Q:���u7IS�4۪�e�j��4���כv���R�r2[Zʬpz�=���\��"�C��vH�}��߱4�Ld,>S"i�U�d(����Y�h)`"��Ϙ70���ۂow����*��wx�(Z�r0��H�ż� 4�G]���jB߭ެ�h ��J��y�O�
�_��P�0*j�1��g���I.;�v:�&�hn8=]y�=Rf#�C�����>1I��
�Z����`��ĳ��A%kɀ����@�D��`�w�:�FD\IH�٫�b�1��EDk��^|�{m8OJ��y��1����~N�V�m����[��F鍻�ڒN8r�'����.0.]���Z"��Bݬ+>��2.���z�NԬ�����N?X��+�p�g�!��2��]͢?r~���
��00_��䉥��W�b\�'���Un��g��o��pLW=�z5�"��S�*��L�;�������ŬV�;�bLv��Ųʮ�+[ӳ�^���]�2�$�U�(�jHW���S���K�{e�J/W���,���/4���������n�<�B��Q@��5����������,m�Ղ����w�wX��da�"ߠb��Ϯ_2��0V:�
B^��k�?�$��R±˭�|����N��.�����N�|�k٦��Jg��ܾ�ĺ�V��o�7��'*Ϧ� +�7?Z�����z]���8�����K�mk�~NW#*�hXA)J��Fڇ��V�����[KA(A!Yͽ�zz��nn6��&֯4F�i
���d��Z�8��	T���_?f��Ԝ6�^^ف?]9J�:��M��q}Q�Тsz�˫DQ�̆l�1�t�h�O$r$��EL;\^���qAdS�F��8�Y��CH5~�p*&����>x@�$�W���i�D�j~
/�P�X �8a[^I�_�-����[o'p8E��1㐠ҪR5�]�B�����(�w�*����'��z��dé�������3�~g-QA�����E'���)ky%@sE�& o�7T�5 (�S��{cݍ�YH���~6GF�*��0�r���`�9�� Q\�?u!�ɬ�Gj����_�D�.5��E`��d�r#M���8>>X��a�n�Rf�=O#��3Kyb=��i���<h�Ws(W<�͑��W'f�D��� D�H#8�2���\ц�a�7k)nZ����<[_������f>�t�j&�^v��0���]R��2ʥ��&ͽ�>F��s������5�E�5D�:���ye��>�����f��g��fc���W�Ps���.�w-��[��:�HF�I*��m��S�[h���k.��z���y�盖��>G8ؤɿ:�ުD�������6j����U��T�]Fzq�2�ѻ��$vo���\���|��l�C��.�A�'�ß]�8CQ��ǳ����O���#|*e��P�H����c�X��������2���ݔ<.�V-���� /�G���2��=�
<��'C����r��=�)�u%J��[�>q�;<x/0�.K4l߸)Q����,�	�y�֏���v	�LmP�π�ᩀ�zͶW%/�NO����|WjU����P��Ԧ	=�/�q�m{%��e���sEԌ����1o�Ǩrʖ�; R|lCڒ�#Q�1_�B\v�#,m��C�m�\~��Nl,�(N`$s�{9jԿzǆ�쎖���jP͛�j��v�I.���**�C`���k�v�rsQE���Λ|���{���x���t�a�B�ym������[s�_��`�鴾���:1��*�t3�m��B�����8���HGz���t���p��)̏�	9.��L	=��-F�(�q���k�-��-P���t��q�i������-���c�|s㈅��^�|�+�yʥ'2)��Pw|Q�o���JK�� 2i'X��GY�،R���N��WM^յ����k�Ub��4��z�ٓ%��s�O2���r#O
ǩ2_[:�^�s�2;���Q��d�w3r�fc��Q5�%�NJaA��j+��<T����y
�Z��H#�|8e�o�����}d���駛��N�]��oX���,ϟe	Ȥ%^�8vi{W\��֧�3R��8������ʜO=����׏v��Y�P��؎F~˵'��ٴa����T�?��y�U%.�	K�;�L#]�Ե�ViO�wO*V����Fr�qWUs\ć<#�8��sEW9����_G&�P�@�ծ���28>���;�AD�+��0��1�A����
M�x�p칫D��KS`>�
�a����W�_�t�M�|ə2ڢ��t�{������'�/V�[7�0-Թ�f��1!tA�C@��OA�F�M��>��5bK1֥��D�y89�],;���=���BqtKC�<]*����l#K_˲�z s�jF���HhEBu��3�ڋ�g}R�}'��R�Z���s7�#�YE�eV����x�<�A�%L���^N9�5���?$ /ͥ�������ŉ9�x��W��#&�g}�p�GH��O��C�`��g�Qi���*�б����HC�Yw"3���6o�Z������MB�1�G�����ɓ�Q��S�����Y*2P�}���R?8K���"WOr3�6t
q}�]����趚�h�>����A�;�E��Ul��r��uKq��3����p��pH[7ab�y}ii���-��k[j�"��|�Xkt�;j32_9��9����6*~�76�az���
&<����-���4P|ϓ�>ӊ�Q���+�y�|gh8�W�H����}t윸7\��;�q�3y+~r�NI<�y���s7PXwXI��aa�3v$ɉP�'SīQ6�7sR{�+��7�y#e۝D>��n��rx$ឈ8��y������Hn1�}�Fz���J�ud46>���O�kx�������av��Y�i�z�����_�0����)א�4�CU���Jl��l#�	>�_Oz>͂��ݴP��g��D��mvE.�e��#��1��t�N������+���b
��c@,+����"Iҹ6Fpr��G\�λ}�_��x��P(�H��c+�3�A�~v�<8�C��	l�+�/��E�����>�V(�z~Kr�K�;Մ�"�s�E�U�`�p�m��l����H�W��d��pu+E�=���L��Z���A2w[��~��S�wֽ����@��2��!,�������n)l�bKy�ͭ��@�M��̊�L�M��p��(��)ښR7)�KUN��|�e~'��P�����NoO/L�:�Z�I�`V��˥楪�uz��e
`�/t�;�)� �=/S�<�և�,v��X|ji"^o���l�1������5C¡�$����(�09���#Xӯ<jMH���l}��	l��U��B_צ��Q0P�J!��t�U���M���o���?1�y[Z�sN���E:�GM�*1M0SJ�&�9�gYz�����O���4A0�/����^qT�G�7����m��	䧎�I`��l�}�Z	�.��;I�f�%-���m�j������ʀZ:��G��i��E�ƣ��y�~w�"�g� ��d��-8�]�����f�bK��u��N�c�{�T�D����TD� �;,�8Z�(82	d�ع랜�kyYA�hٷ��^�B���x�c
�_��Z�s�y�s�n�'�,s��Y������#�r)�p[��H8l�o|�4.-���I��S��\i�����pX�P�+�{M���pFv��X/��T���aK��VF3o,���}���y�m�`�<�@�����V�}�g�gۇ;�p��3H�߱����d�n��#�
�B���F1'�<koE+F����@Gؖ擠g4�z��(�A�f�����a�/T���".?q�<.�#Tg�ε���.��C�|�G�@�)=� �bIa�=LTO�eq��>h��wY.����<���K�r�� ��p�����ɨ]"�%o,'￘	�<���C�蛤��v�U���_�MY׎��p�ԗc�JU�z-%=���B�a���,���d�u�ֵ�	�����R�~bG���xJ&�m��g���t^�� #���xa�c���S��su�B�
C_�����bB�C�h\����µ�iÿ-�e5]�}g�c`�����(��8����.�r�Rf X��Y'fԠ*V4*�Nt%�}���j���j(�X����E[�$�d�J��������|.kUi�X�8Pm���)�*�����7��������Ò�o�퇖/�YWw8��e���|��|"l�ؒ[2v:KC�h풱���Ǐ�s{��M6��AK
�ˇ�����6×��&����|���;�β �%OueǴ�K�h�� �f��GK����0�t�Y9���Hp!t��Oq�XV��6�y��Z]�_�־�uG�4me��K��� dDI�JL{lZ�u����ZD_.x�~(����7R��M�,=�����en�r]��N��hA��'��A���6!�-��C�@ҡ�F�
{I��"�;*	@J���j�V��M���7�	ی@q��f/��|��5^X��3����Y�ĩ2�]E]���~��+�Jp�^"S��]�eY��D.@�a�^�)2�Yw�\�kj!뵈�Z�	hA��QQQ�	d�%�	'��<���b?0�}<x��x:����]FmS��\$��u��!��}>XH�&b��O�n_�����N%�*��+�����f���_��s��DR0|e��u�@"��'���@���#gu6p)n�>��<j��*ϿZ�D�_��=�t���|�23���g4m��5�T䮥�jQ)�l����l="���VQ��X󋜞{m���l��3���c�Ebڶ{L]�P��������xzA�;@��os�=��_�r.4�
	qoZ�|�[V�Ac�p�+�I���?ޯFx�W�w��G�<�� x��i�ƝƧ{>g�U�QQ��,F�Sֿ]��A�8oU�XҦ��ċ��`�}��јT"�����W-L�CN*/�	�.'kM���7g�$5�wH�\�̕m�f�E�k�Zn���$�<�$6��Ew�� ����mv�;k`�Ѩ�]���}@c�f��bOU94��blzl�tP���ǘ�nв�7ZD�χ�y}[�����k�`A��9z�m.���u�W��5�>G%��
��e�_���T4�<�	B��K�h�Ŭi�C-�Zy��4�2��v)��p��K�W\E�ە�Z������𙡠��mC�F'b�As�Ѐ�[͠Y4(=� � Q�C�Ru�R���l;�e�L���7vT�����>菪��ɍS�SW�͝��ʸ�����=�~��#��� s��p=uW� �bv���	�s�E�o�#F����"�v�T�Ԩw<��� t��J���@�?�)W�[^[�|�f9�I�c�5�^iR�_�1)�gn�o��9��d�.tڦȘd���-��S�=�g\�YO|b��9
���DO�x��`iU�`aCX�d'yu �Ԑgk,xP؛��Y�r��*h�Q�s�8&��ܭ}ߝ������Q�a�qoЇ��i�:ǰ�  �/����)T_G��d~!T�[L�~��΂<�K8������I�OYl�����	\�K�9b�#/<�w�=�u	{�Th��Uq�|�P��P�c(��"�u��Y��M���Dz���x|�3vy��H�+%�m�����jw�b*#�����YɎpU��ڲ�!�|��_Gu�U�0h��u樂�)��u���a�#���$j�׾X��~��Q���Vp���{c5�c[�쟚0��U-@�)9�K솣[�v}�.v�ӎ��ר�0�%C+�Z�`+-��z�&�]gD Y�n�����?��^�yUET�I0�������j5zZ��k�H�!�����}R�o�AhQ�-�%{۽��ɰ뀾3�W���&��m	E�p�, 9p�Y�xt~R��VC��{Եc�	;޹��I=�{,V �"�Ɏei�QS�Hs�[$�o=�1�e��\d#�UbnD����Jt�Jt�/p4 ~������F�����4�Ti��\�Q�|�n��V��s����8�D	�Fy]�k6q���ȉiyלz���Y�ߡ�QՊ{�ո�0sG#M��>�/�@�'��Sԓ�[~���q&��K���P��M+t��{����ܠ����I!?'��hꤸ�W�/��8�����cY��5n�������Y�0kJ��A��A���6���+J�C�' E7V�5T�RE���B����d���V������=A�gA�V��p�|*���܃c��{\�����z�7��u���'|y˓�6�9SV-t5�-t�'�yc���rΞ7��B��y�j�t��2"�lʒTa�VmP��"�i.ߦ+j-����#���0�@7�	wށ\��b�[&-3�X%E�_�*kǓ���s82���Z:o�3��.j�$��N��i|����9����z����t�@��@�����݃ˏ�����8�|���J!��6r�6r�<`�K���u��y�[�}�0[�����RM�?��pM������Y�����plR�˵߰�MO��H�m�����W�|9b�cb���,��'=視U�KʇU��泖�<(�4�rq��k��ߡ+��<.��=;5�{Uѯ��L�ZoF;V��NY}���~�̦Ce� VWdj4j�Y�i�kӹg�����m6an��z�z�>ΏiWhQE����➎��=�&��x��豉}�b.��t���z�(�?���{�#횞"B0^�RV�B�5��I��{ɗ�]D��K%ۈ/������%��7���r�DW�?�`k��h��"����U���J��!G���[��X�z�D��v�l���'Մ�2.P�,�����4,�o��h$Vq�WބW��ئ��hd��Y:V�!�b����
��eZ� "d���<N�"�ee˽�5�Y�c%sٕV:�pA�:g,��L�B'��m���ʸ�ސP�-�q`�;'9���P����wд��ý>�H,��V%Ehz5Oe�(V8��pr�6�.x�������ʿ:����˧�ԬD�|[Dכ��9t��5��t�v<�'�!{7���-&�L�2�
��ΐ��SE9�뜾7��N��V_��tx78A�^�53�|�T7����r*��qp����9�m�H�_�`T~��ce�ɦϔ�jJM���F@\݉�fk��IW���o��`��=���?��Ͻ�B���_�V�FT�Uk`W˿.�w�x�݈)��9Dw��Y����r"���,��
��YmMZ�9<׳��7R����!��I�ʆ� ��`��}~�-���Q�h�� ��l���_RIhu��y[����B��3���3�\�ٸ+�b�\��)��I��>�f���}�<�>�ݠ�/�!��W$�B:�n��K���%`m8��d%T�!Y��h���	���9E"�r�YF�6�c�0�=E�d��@�M�7����2�u.��[�+,Έ�_�����t˲������=���{���4�EC7ؑL�9v�(��ַ�t)�kJ��|��5��j��j�>���Z(Ϣn�ɠ��R�eiZ	��,W}"��
�������dҫ+���$�����ƴ�y��掣�t:"|߿&<�<ٝ��]V��/��*�.ao���Ɠ����.Fg�3Q ��Y�t�J������pc�lp���������l�\��y����`m���$҅\������;6
y7����0�Z���!�\�\V��@@�����@;���~�0_��o~(��]�
֎� ��xK�ʚF۹� �X�3=/ܹf(�5��>O5�jR����'ހ�����FJ���W�jq�j��#\P�Q��Hխ���VUV�݀�P+�����I�B�?t2�T�y�Zܔ��$S�$�=�y.����RmW�R���9=������壿.;�t,�	u�F�)�G)�*��G�jNѸ@��XR�XF�+$l��M/��(e;K��g��HbG�D �B��bAZZ?�����GiF���T��Y3�v�,B�C$�^����z|Ű�� ��� !�����M��u�N\�X�4���x�x�9r7�|-��k����	T� ��fvq���ͳ�Ϳ�-�T��>�ë������r�xhαWdTΚ�;��ΰ�̷:<X�_ �~SK�������]ꁓ
%��f��%J�K쌭u�c���4���?�C�>��V����P���N��KB�&��N��֟y����c���������z�n�%�e�_�@���s~��p;�Ud���	X啵J�Ɲ��m	=g$u��T�)�B(�� \��������b:� ��k���v�-�����eɧ�"��i�u�¦����PT�ֽ絔A֯�)�7�.�ݵ�����gfs��S^P�O��,��f�=���� �"b��<��}:���W�>Y��\��%E�ٽ&�o�"fྏa� Oy�����q8���)ސ����w,�!����%ğ�X��5���q�;���X����lǩ-���I���EFe��5�Aʿl�k�C�D��n�Jz��\(HZ�� n�ha!s�,��w�]����<�j*����I�s��N��x��z�����E$���gMpg��O~1֬�R��	2k���sE�W�^�8�)h�k��l�S�	Gشa�\��)B������l��0���1�<Z��Ϻg��Ȍ������w�FXk۾��H���$�k�,Ae�4��F�[��
�	��}
�C�@Kz�lկUd�̎/d�z��,��Z<���Q=7@n���0�9EU0��6e:�YK'n���*(W�	��\:�a�������K�~������.@= ��x�"��9�]�����0:d���Z��B.:81�B�-o߹�1nƇw��*M�k>N��Q`�fK��}���U�Qȇ���>��1�wP_�H�9@R~*
�(h�>\8� �/�6T\ xRO�Pd	�,�b3H� D���D�~������g���s�|^�����e��2یd��BA#��b덷v���[{ػ'��b�����>&�vB]�7eR�Qx�s��\0z:3��nE�P0�1t1����¾3�ft?��uҹO?ן�l�{z�@���g�����*���J�SOPR)�
Lc���{�>�F��x��nlh���'$���x0��y�ރq�Y��ȽnW$B踱��쥡Z�<C��j��8+sc�S�_2�tM|Ϊ�`�Yj��*g���gwk��.]s�ϊ��������i����|�t�����^��o�5�Qk���i��/$��̹�բ &Q��_�B�$\��3�
�]��n=�h�e���T�ZM`�2�1X�jM�/%3�c�8'��=��o׹�Ҏ���F�:��J���O�i���7�0� ��k�qPפ���g�:�V�S@M%G����MT��N!qm����c��u�}oV�z���K*UU�x�$��0�g���DL3}�zH9 m�m�h���I��Ч/���&�Q�[enO�_fA�j�T��纙-���������_V��;7��f�p���ٸ�3�8W��\J6����7Z77��S�S�6/�t����7�+���D��r����T���~��C�#��y#�c9�n.�W��F�k:U��#jc�2�0�1�
@b�6)1�BL�|=ۙO>р����w��2���S#����kA��L�D�o&�ۅ�*�v�Q"�6۹��ˈ�
��IHM,��a7�M�:�ل�6����;��|���Nc���YF����YcǞ��9��B��-������?���No�i�U�^pP�Q��+�/����Kw*GY��j.����ן���\q{?v<L�1���xI�"|1%GX�?�9<�d?b>[?�e��:Cg~���K�T'89��ńK [�ՙL�t��V�wN��/�~Z�g+	Q^��ob�2;�"?��Sg�S>�Ɗw�,���py�g���:��9�yt#5lxA��_�n� l�9K�;���_B�X����H��
�Ѭ?���m�_�ԙ�᧪��8�����z�dQD�?h�v�螶�2�ꚱa��/2�< ��ݬ�{����6�Dk{U���c����-}��9����9��p�TDZ�q֩�Wm���O��/�Xs|��Q7p5���[�a��'U�4D6�TxWw�=�ԭ�MdYd#qKZ0O�l��;�*�e�n/U���K���>�	�YW^��ƿ�	�����9�Wn��2 5�f�����/�D�!�t���,x�������;��m���8�A�eL�f̤���&�v:��C%]���S�}�_b��Uc��{J��gO�*q��
(GT:�	.�q��X��K������?H�3������)�UC�P�S��v�#'�+�Յ$�:�`�d�����X�H�s�� �u&�(�9�}��7�~~���ʢ6g谹��o���?�� ���U�CN{�6�>qS5��l���נ"��?���f�XY
�+�����ȅwT����fa�{Q:�@a�ܡV��ؑ�a��1T>�C����󷶙]�>Ĺ���4�����֏>���@}`Կf�@N�!'�Y����F�+�Y'�7��V%]"iI�_�;�1�h�==?�-���,� �r]�cw&��L�U���jц뭩��ݼ�F��h(�Tx���+RS���5����	K��Z����HH"E@x6<���xORK���ɱ��(���i-�[�����g�1�#�����d��1�ת?~1�*n��'a8�ֈ���Xy~_�����ުv����rn���j���,WiX��w����?����iAO�����E�"_�\iU�#u�3�̓���
���&��+��v��'\��z��V�W-��i\�I��`�X�uH泇��9j�����,m�E��.|�uIbA����C��*,�]ft��]��}�{4T�aj��OK�)<v�s(�gg�����f�j�S�P���������ȖɌ1p����+z�w�)�K+������	�����i�ɒY�t�! ���*�Qq��脭��z�j'H!��F�(O"�%[#c��{�D��\�q�ۯ�o��~��U�ȝH�~z�6wf�Y����iF;V�y�{l)+@52ML$k��#ˆ�Ccc�v�:���?��¹G8Z�� F/|'��ʷ!����mo�䝧����6=�~�uҊ�
p�.��s��Tg�]�Yg�4SӀ�M�B@�6��S�7�}�V��0�P��*���t�����h�[!� %��r�fFH���+,��j5&�ӝ�0���L�
�X�X�-Jm���j�z�x�����F�3�d"mD�F��Ơ�r�+�h���+_����4hl�V2�$xx��F�~��K���	�U������G����
`��B���"牤�4Ã��dd,�RT�e���?�N��Z����87Ǣ+��0�v�zU:X!�"��-6��|���-yj����$��<E��[@�[������ջ
�����2x6 ���q��_W�X}�*A���	���o�Ay����ݻO�X��j&O�8b�/W�o���ƪ�u�B�}��G�j���ȱ�HN�o�xd��~;��u�� ��<�Y�p�_���N���&F�Ά%{%��ťm�py0�{�2��m�� f�|nF��Z�V�.g��<���(#������sk�k��uj��c΂;������<�a�Tq�1oX�(�@V�B"�_������%`�@���ϱ���>`��*2�j��������r�SFd�"�1�O�~�J�42����-��q�ٗ>�
�o?d�֏�j8���i:8dI��v�kI�Y��!X%s��}f2��2��p'�+{�Y�!��m����=�-B��	Y)��xi@C�k��_��[[��h��9�;J�8v�ۡ�������� �o�N��~�}��ki��:��٨�����a|�Q��芒ʺN�Aݳ�ܛM�#�a���z)�-J
��y�'�V�.Ӻ^��Ⱦ�`|�TS�sQ/3���U��f���2~���ݧH�<P57`����}���3�V�#Dw]o�az�e������ď�@�lu����x������Du(�����d�W�=���D�N�\�Jr��'��{<D��x#Խƶ���]��9�i�t��-�PDz}���R�&~b��xU�R$����<�]�o�cw�����~�P���OՋ����>���u��� ���uT~�+]��(�v���/�%f�=�6�j��[�D�փf���m�i3P��6~L���r(Stݽ�?��x��U��}Ą�6$�>�ef��
��ocR�b�٬�ެ��*�Kv�LȂ�xh���ʕ�����ED�d@��'W�2��"�H[���iד���@�L���B��p�]"u�����e�F?�Td31��TĨȵ�B�[�9� {�R�6�-���XHqi�o�k{q��W�H�I��-D��D����-�c�:z���k��B���jD葆WMf��d1�zGy_��������b��ې��!�����F�)5����8}��,L/v+���T�����1 >��w�u��HT��a7�e"D�f�\_��5U8#��h�:�+��_�lD�P��J�ެ<�Ƞ��ܰ�g� ����<R�����'�PM خ�����Ld�$�?Tn�FJ�绤�¶&����M�{���\�� )�@�a�{;��	>������*Q(Awo�� �%;��.��oˤh�l>�)
k���]�#�_0η��$6;��Wn�;��Z����!��\�	�H�qU c�-���d=4_�A�I�]�?������E�>ْ�������7���G�l��#5�7�!�|>.�䬖��h�g�S�?������6VA��Z�^X� )ߏ�dO�ʝ��ub���9Ŧ]#Hƿؼ�yN;CZ�b�#��^ߙ���U�ώ�:����ӗlhn
�g7��ѐ</`1��K��h1@ƝKLS�`��w=�2��)Q�r�h�w�&��/���H���Q�����������p��������|�#[�xm��J?]M�͏��X	�LЈ�"��j�Ρ�����ͅ�`��,L赿���/��$�ɸ��y���;�Lު6�湧� ���q`1,�C�Vt֖�A�.��{�
A��&ׯ;����|V�A�?��}f�i�!=?��/�:�=X��a�F|:a���轃c}��l?e��e�HZ���D�ώ����`0XZ,�=��c�2���Jc:�Φ��r��u;�T���(?�����ҭyS��{V���bh�Z_ƳE!�_R2v���$l�-�L�׏�b B=ՙ��LܨY��Z3��d�O��:�R�O�����(���~���|���&�5�e�[{��#���d���,�ݕڦ�����mق��p��${Pj��|L�h�,|���� C��ٹ2}��3YP!��B�����s����lH_�N�2kc�+(��nsY�.��t��R�KL%P�tG%���Bdh��ִ�5�cxl��坈�x�c��>s�%���9#.�a�>� �Q|�L�U�Pԟ�פ� r�x�<�*LF_��w��X��OK}%P�¹C>�y�\���&�[�)m�8뱊�Qv��!�W>�h���d#���"6���H分D��8E~OPַGZH����j�⢵��5V(�Qc��濗:X��)$�������sm�ƛ��N��0i}}��L�3>�T���9�f:e/e z)��91i�ȭ§�f�2�(��ŕ����'��?�6o������b�{��k�v�;�Ŀ�ɳ��a�u�9y�e�&a�b��_C"�N�+/c!��8a��>�{5���3k{E��8`���74�ZU�H׻}O#{L.���R<6�c�nb�Hy����J\<m���W�~w2����V��8݇M�CG�Yn�&۞�m�[�q�a�Xad0��\!�.a�qi����%���*��F�Qz>�����T5���F�RT���)L�gA[I��.��pq.���F�"���!oH����d1#^�w����ZE��W��BT.<��T�$��XF�#�4�"�����bR�
�8����ޕ�N�M�˱�
r����G ��8��E�o�%�_6G<F����~~/+{���]��B��� +�<����dтRO���OGF�ZG�?����Z���*Q	ַ�5��˜ ׈��"���D�ɹ8�3���t����Kx]v(g����`%����hʪ�
D�P%̂o/<��{��p�Q�C�@&����8M1�|��ת�vq�>����}��d4�<��Bq��C��ꖲce<ԗ�gdQn}]�����u6�x�ql�P��2��cs�|�#;1<�l�y�ܼh}�V���{�Gm��<��A7�h��&��D���S=�c]/���%����h�3Z�,�Z��0R�'�ѨH�;�<DT "�L�h� �U�uB�AR쐆$u4}85rW\Q���@�pK�ܦT qkU�K��I8�1���/�tX' ���"j����	�F.�\����>^����le!UY�^n*S}{w�T-J�0��Ӣ�v�Z�'L@q=�55�5�BT��S:�7��`r�N�
�o���HS��N���5emH��]���Q}�o ��`^�iYpN�݊����|)��	�������G�����*�E�w�B��	YN��
%�/~��%-� V*b���PKF�I��|  6�  PK  o��U               word/styles.xml�Uao�0��_�; �U�PuTU�*6���B�:�g���;'1KIX)��/���w�\.�6����X���κ$�T��rDn;$��ʄ
%aD�`�����zh�V������d��a[�AN�� 1�*�S�K����$�(�b�\��n�<�)�$���rΌ�*ugL�JSΠH��{��)!AΎ)$��i�;�OS�\p�-�!QΆӥT�.v���1��(v)]	g���0ղZ�J:���2�G�/�`z%�9�e�����r:"3�T�G��ߢ�ć��c*�.��g*�Nb�����~	ٗ0���c��e�@v��x�:���<��3ޙ�����8��A﯊�WZ�z���Vg wu8��*���S����i�ը���.ՙ��MO�,
�$�!�U�E߿o+ĵ*�<Q�	�g���,�$&�݊gM/h] :|�["u`v�~�pJ@��|���ʄ�(6��+�m��2��!���_�H
0��%l�aCv4,Q3��
h��P?:�����|�mޔ�q��/*�t�����ufӆ�A݈�~�ݶ��p]�7�Gy�椋']g�v=v����Gߔ$���K��������99���m|���=���P����F�Iۦ�!�N-uB��H�ڀ�E~���h�G�����w�;<ء���أ'ߩ|Me�[%�߸:��� �l��x	�C�/ZOv�PK	���  v
  PK  o��U               word/numbering.xml�Mo�0�����vh�&4*�e��i�vh !&A�6�M����fi��O~?�ǎ�s����=�,'8��3�S���6�O7�1��MRc�
�_}�;,q�֐���h������ҲX��(asRB,b�(��n�����2&*Qa��Z(�18�!1�(^{ܠ<����ߤ-I��)<m��pS���7�RX$\p�]^���^��mJ�,���*��R,�΋�����6ǿ�sZs.�;�''*[���������q1�X�kI֌�$�?*4�xz܈��)ž�\1�匸a���>)�$k���:MVe	�w�9�MXT?��S����4�-mg��f��I끋�6G��,\�N�Ή9ވ`ݧ���]�����m��;��<���������4GI�>�;���ؑ
V��Һ:h=-������Ci=����V��ᡴ��@��*ZJ���ʗ��u�.��Fʷ��]蠍t�z��-%�Ci#��ZhC�[J���ֺ��N%q��%1Jb��(�Q�$FI���xFIt�:xǤ%�Ğ��I'���xDz�I� ��t�Z�G�)��-�#R�N�H�t���V���7�b��(�Q�,FY��e����,�`�̳*�γ|'v��i83Ձ]���Y������������������������������)�^�����~�zaG`�̫2��2WQ�}\�)ʮ>�=�������m�����oPKA���  �-  PK  o��U               word/fontTable.xml���n�0��{�(���a�*
�6q�8� �ui�$��@��
L�Ml�$v�����t���A_�� �|����B~,g��Rpо�=r,���q������s��	�͕��y�-�X����Jk�!U-a	�Q�Y5ʲ���$C��`]�^��8��(B`u�pcZ���;��^�hzi��C'��i�7��&�C�V�Bf�T�?�ݟ_�o��	es~�j2ze�PRG��b�Vh��ѭYO�%�J�ŝa�%�լ������=U�0�ճ�e�*�lx��;ӞSƎ9�������Z�4�P
W�TW�����7d�[�� N�|PK���@  V  PK  o��U               word/settings.xmleP�n�@��+�����"��О�`6Y)�^�R��5���z�=3�W���'��)�f1/M��Q��6����,�)bm��f��[���������6�H��e�a �S¨XK9�h��v�ܤL�Uz�,��G�֕_D����a=gY{la�e��PR�	��<�����9uA4��<�Dp�o��nWb�����?�����4
��������\%���;��27��������▢����ʻX^���|��?��w��PK1�	  �  PK  o��U               [Content_Types].xml���n�0��<E�k�hKQ�r�rl9�se�	��ن��w� T����=�3���xl+��Z�
��J�Nڎ#�Le\·���9���Qk0�h��J;���{B,[��6U$Freu�i�DS�I�@��v�0%H�8ψG�G��p���+_���C�筆1պ��:%�:�= \�l��d[Y��2�.��W�;h9�3��w����%e 5��݆gM�q/T`y���4p?uN�b��űHo�?�N4��8�9"�tC��2�%)��� ;՛-�S�b�
s���2�v�; ��ǔK럦u�i�2k�]�vA�l�C@�))/A'm�P�@�! �! 7! �! �������6���6S�30(	_��XD��S:+�x���ء���j�b[�ր��oPKv$q��  �  PK   o��U�r�D�   �                   _rels/.relsPK   o��UX"g  �               !  docProps/core.xmlPK   o��U ԇW8  &               �  docProps/app.xmlPK   o��U�� ��   �                =  docProps/custom.xmlPK   o��Uc���  �                 word/_rels/document.xml.relsPK   o��UP��4  k�               y  word/document.xmlPK   o��U�}�f  F                �  word/media/image1.pngPK   o��U4r �(�  g�               �/  word/media/image2.pngPK   o��U�����  �                �  word/media/image3.pngPK   o��U�ζ��  ��               � word/media/image4.pngPK   o��U��+�`  9i               0H word/media/image5.pngPK   o��U~m$B]  �f               �� word/media/image6.pngPK   o��U�}�Uk  �t                word/media/image7.pngPK   o��UF�I��|  6�               Yq word/media/image8.pngPK   o��U	���  v
               �� word/styles.xmlPK   o��UA���  �-               �� word/numbering.xmlPK   o��U���@  V               �� word/fontTable.xmlPK   o��U1�	  �               C� word/settings.xmlPK   o��Uv$q��  �               �� [Content_Types].xmlPK      �  ]�                                                                                                                                                                                                                                                                                                                                                                                                                                                           documents/cover-page.docx                                                                           0000664 0001750 0001750 00000014203 14342054664 014406  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   PK  �<�U               _rels/.rels���J1�{�b�{w�UDd���ЛH}�����LH�Z��P
�PV�3���#����z�������a� �u����M�h_h��D��b��N�
F�����H^�#�r�s�Z�1�y��i�0��n�Ym����+�v���׍�D[-'Z�T��8ʥ\��D�e�\����K3�e��� �{g���S�K.:
Kv��c��\SdY���D������i����ɢ=�ϚE����}PK�r�D�   �  PK  �<�U               docProps/core.xml�R�N�0�����REI*�JHm�f�mj��v���q�&�P	ɇݙ����� *o��Z�(
B䁤5���z5���3�HF�ZB��`Ь�ɨJi��E�
��`<g$MJU��֪cC� �	�B:rSkA�Ku��_�����Kpk���,-�NW��* ��Q�ւ�ꅎ���\��>>
��	�����#��x^v��\�OE٩��j ��Ҿ���&�O�9*�0��(���*�K�[w�3��~k�ǵ.Z�������+�vؓ��+"˝{���^v�jWYcn����<�`CG��;R�'�*N���r�����a�ۿWL��c�vmv�@m?Ҙ��r[A��X|PK����h  �  PK  �<�U               docProps/app.xml��Mo�0���Uĕ&�P:��C;!i솲Դ��$J��t�X��ɯ_�q����k�3X'�*�,&(%t%U]���e���y�*�j��CkvG�V�^��A�5ޛ�N4�q[�m�}����x���8u�<N�0\<�
����@\������ܮ���c��δ���/,��m);`)ɳ��4}0��������^��e���8�l�:]yv��Ѩ�^���LO���	�cXO��f�EL��)���-����5t�m�؜�S<����X2�s�G�����y3\��Œ��FV�gym�iK��ԛ��%�PK���n:  (  PK  �<�U               docProps/custom.xml�α
�0��ݧ��T�Ҵ�8;T��޶so�M�}{#�>N�=�C��j�/+) -'-o��8I���`���,�v�\#���, k9�j�����9c.#EoR�qR4�����:T�Qم�"|9���5�Kd����o!{m�~g�PK�� ��   �   PK  �<�U               word/_rels/document.xml.rels��M
�0���"�ަU��nDp+� 1���6	�(z{�Z(����}�1/__��]�m��,I��Q�Ҧp(��%��I��NR\	�v���Dn�yP-�2$֡����^R,}ÝT'� ����O&�U��ʀ�7���m]k���=���n�H��A��>.?��|m������������?@��������I��wPK�/0��     PK  �<�U               word/document.xml�[�r۶��S�h��8S�������;��S��Z�m"A5� �d檯q^�<��@QN�V���nucI$�X�Ϸ߂���ݖf�X��Ao�;�W�΄��~�����:�2&������w�_};O2��%WP���>��F%6-x��N)R����N��D�Hy����W8W%�~���+��^�M��4�~�r����}�%s��-De[i�?ZV�v�|�U��d��)�QʰnɄZ�V�0�Y̨VY93l���]EN��N��@�B�]T#Z�KAy��{�V�N��a�Ό��VZ���ے���"�U�щ��5~�Rý�i���>M�R�_�5���2MΧJ6��I�	�� %�1�&:k������v��0OfL�.�t����E&��p鷴� y��5Cr��g�k>v/��r:�wx�J���<��H���{�=����X�QTn�����	sh8�c�{��g��p�������:/+ۆ�`4zB����5�`�6v�Sog�~��x
:�1�%�6���k쿁��Zm��N�/�~���~<���������x�����2zjX	W������H���j�7�oz��`j�y��e�@R��� o�	����`��zn�A�#�i�Z#��C
l�k��N�2	��>�Y��p���,�@�M��F�S1�
,gV���e��~OA��G��6���A.��`��
na�@�-���9&G�F	Ul��!���RA����i���p�\��M���k��S��d����S�<gXJ@�⚸W�iN[)�>3���s���8R��V�3z-�x.z�QA����͟ʚ�\�� �*�$T����M'R[[��z��5 }���;R_~��b�j �_
�ao�b���y�f�F��C^+�X�ܠ�F8��O0���gk��h8z�<�n��M�V�h	�S���2 �hW�B�\r�g������6�|�K�#�ӏx�q�5Vk]���W2���{N	�3F���(�M �@4��aq��ɝ���^�9㩂�1�up*$��/C��$H� Znw*f-�Vnt����	{#O�|	��J��c���R�M!]'���X�yd�R�41.o}C�@�S�z�˒�ȊQ��\Ys����hc8�|��g��� �U?P��ԇ<��Zn��:!E���"�����,
�X@����B����mC^�#�#��T $ �'[0H	]�O��
A��YZD�	'i~Z�ՠ�������(+4@8S�'�u��$Lx��	�b��cN�.�&]�~�<��Nq��� ��Y�Έd`�E���'mm�X��RTN�0A���E�8�W"o|�Hԃ�ѫt�R��Z�!a������/��d�!5��
bd��M9\-�xJ�����*�A�Ɠ�d��*����~?i}�5�gz�q�Ycr�J����Ɲ&�.���v�6����&��wM�}�S>b��>~����}�*8]X�?�5�fFW����B`�oQ�-��~<����i�ܭY��4�[{�j�hu8���}/$�s�V���N�MhĘ�~��SW�-˩�O�m�v��
�F��{��y�%���+0c!7��DM���K�+6�Z6թPL�fۃ�+�I�L^��Rآޝ4�o�!��l�w�=�ZH����� ��Rg��G�)l8�K�m��u���e0��n��UH^c��!��пn��\���.l�X�vM��)�x��t��Z]�Š��?~�$���刣�p!�
�9���s]���B�\ҿܡ�d��_��5�մ����������@hN��Xz	ċ@h�g�f��bW��I���8��G����h��~{��c�3�>KX
�3�1<*NКS؄�ְ3��v�X���Ѣl��h��RlCپOBv�ZT<#�J��n�!+�z���x`S����w(kqqgM�0��p�mS0O5�~�w�h��ho�-��_����tV�ܣ1FL�����a ��i>����U7,׺6���2ތK]��8���(>�X8�2�ѵ�ȑ�M���0���>f<	�3��A�Bv �9��#%����p)�y�բ7B��#:o�~g�~��y��ǎ��PK�~=  2  PK  �<�U               word/styles.xml�Uao�0��_�; �U�PuTU�*6���B�:�g���;'1KIX)��/���w�\.�6����X���κ$�T��rDn;$��ʄ
%aD�`�����zh�V������d��a[�AN�� 1�*�S�K����$�(�b�\��n�<�)�$���rΌ�*ugL�JSΠH��{��)!AΎ)$��i�;�OS�\p�-�!QΆӥT�.v���1��(v)]	g���0ղZ�J:���2�G�/�`z%�9�e�����r:"3�T�G��ߢ�ć��c*�.��g*�Nb�����~	ٗ0���c��e�@v��x�:���<��3ޙ�����8��A﯊�WZ�z���Vg wu8��*���S����i�ը���.ՙ��MO�,
�$�!�U�E߿o+ĵ*�<Q�	�g���,�$&�݊gM/h] :|�["u`v�~�pJ@��|���ʄ�(6��+�m��2��!���_�H
0��%l�aCv4,Q3��
h��P?:�����|�mޔ�q��/*�t�����ufӆ�A݈�~�ݶ��p]�7�Gy�椋']g�v=v����Gߔ$���K��������99���m|���=���P����F�Iۦ�!�N-uB��H�ڀ�E~���h�G�����w�;<ء���أ'ߩ|Me�[%�߸:��� �l��x	�C�/ZOv�PK	���  v
  PK  �<�U               word/fontTable.xml�PAN�0��
�w����U%�	�@��d�#�I��q�DB�B�f�����r���0��T����I���S%�����Rp:����<#���nٗ���"��}%��R)�:��o�V�� �o8�އc�F��ZŃr`H2�72����'��R����ܘ��jH'�����{��{��P&��Ӂ�dQH���{�!�3К��q�A0p�x��������Nz-n��I�i�ɳ�7��z1�l��`��
6n:�|�[M%�ߺ��ɀx*ص��3<x�	PK��J�  U  PK  �<�U               word/settings.xmleP�n�@��+�����"��О�`6Y)�^�R��5���z�=3�W���'��)�f1/M��Q��6����,�)bm��f��[���������6�H��e�a �S¨XK9�h��v�ܤL�Uz�,��G�֕_D����a=gY{la�e��PR�	��<�����9uA4��<�Dp�o��nWb�����?�����4
��������\%���;��27��������▢����ʻX^���|��?��w��PK1�	  �  PK  �<�U               [Content_Types].xml���N�0E����[���@%���(kd�Ij�����=�$�P����̽��8r>]�:Y����\fc���FH]�e��ސ�d��7|���d�����(�3cAc�4N�������V���)7:�i�d��CɖuH�x�rQN���/�
¬�%g�4Vi��A��WZ�K�d*����_�L���H'����w�����g\���s�)l��q��y�>�0|��x-����Ë�Ԣ� �0"Z4e)9��R�$��h�X6_�`�����@��q��٭���-7��Г��n82��]�	�Ť��æ��� �D䜽տ�ۇl��w !��/��9wF9m��PK5� �^  �  PK   �<�U�r�D�   �                   _rels/.relsPK   �<�U����h  �               !  docProps/core.xmlPK   �<�U���n:  (               �  docProps/app.xmlPK   �<�U�� ��   �                @  docProps/custom.xmlPK   �<�U�/0��                    word/_rels/document.xml.relsPK   �<�U�~=  2               '  word/document.xmlPK   �<�U	���  v
               �  word/styles.xmlPK   �<�U��J�  U               �  word/fontTable.xmlPK   �<�U1�	  �               	  word/settings.xmlPK   �<�U5� �^  �               Q  [Content_Types].xmlPK    
 
 }  �                                                                                                                                                                                                                                                                                                                                                                                                 documents/Final-Project-Screenshots.docx                                                            0000664 0001750 0001750 00000541075 14342057760 017325  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   PK  �@�U               _rels/.rels���J1�{�b�{w�UDd���ЛH}�����LH�Z��P
�PV�3���#����z�������a� �u����M�h_h��D��b��N�
F�����H^�#�r�s�Z�1�y��i�0��n�Ym����+�v���׍�D[-'Z�T��8ʥ\��D�e�\����K3�e��� �{g���S�K.:
Kv��c��\SdY���D������i����ɢ=�ϚE����}PK�r�D�   �  PK  �@�U               docProps/core.xml�R]o�0}߯ }�4�4�ɶ�4�%b��+W��i��_A����{N��j�8V�w mD-y y�Y$h�-�9�e2ge-!A'0h���\Q^kxѵm�IC�J��ZE16|3�SHGnk]1�.�b���#Bf��rfn}5:��e�GK��eg�s%T ��a�ւ���s���=)�)�Q}4b6M4�N�����yݍ�ٮ�J�s#�k`r�о���N��%J#E~H��>g�:������ְ�k����8õP�ݰ'$.�,�n�)H��$c�=eɌ]��o�'�q#7tT�s���$��<dB�������h�^:튎����?>��~���
[B��?�1�PK@�.�g  �  PK  �@�U               docProps/app.xml���n� E��
e�Gc�&�C]Ej��Iw���$J��$V]��j����0����+�,PF( �U-dS���u�D�uL֬S
t���l��`� x��j��+�-o�g6����A��9/M��� 8�(~�A:�DQ���@�P��Dqur��֊_系�=��z�1�࿰T�u���K�yԺ�9��_�n=p�a&����s��̪�>�T���N���Qt�<!x
��wîi�#n�9�eX�<d�Lmi��!yn�a��4Kb�'z��k�5㞑/�i����kӭ�ז��b��PK/�h�7  #  PK  �@�U               docProps/custom.xml�α
�0��ݧ��T�Ҵ�8;T��޶so�M�}{#�>N�=�C��j�/+) -'-o��8I���`���,�v�\#���, k9�j�����9c.#EoR�qR4�����:T�Qم�"|9���5�Kd����o!{m�~g�PK�� ��   �   PK  �@�U               word/_rels/document.xml.rels���j�0��y
�{-��i�s)�\�� ���E��mi޾��ց��`|ܑ4��0[��@>!D�,�E�SV�V[��k�����zU�� 0]�����76r�#�cQ�`D̜�N:��4ż��B+�|��؃�7���rNmAIs��o�uZ�,މ`���(���2gɇ�����ڤ���h���E���a�C9ŰY�a=Ű]�a3Ű[�a;��8'C�,6�mq�HS����K@L�e�̫rEXU�f���PKRr���   �  PK  �@�U               word/document.xml�\�r�*}����|:�e)W'�f���>ݩN��1B�t ��|�l@����J�IE��!2��fq_�Hz��u�ђ*ͤ8��q�� 2g�<��}���q���"�\
z����<����<����0<=��Q��\���X��QR�¼!��ˢ`�v?Q�C�F�1�|2�2Ȇ
H+�����*'>����IǇE96�WW�ѽ���5��V�)u%U�(I���5��֘���4�G���!Gs��s�W[E�y�7�-���ѵ������n��[�k�>)�6���ܧ�5V?�ƶX=�`������4�5T7��q����4{��dpP��y)��3	� [=�3�P���o�.��\�5�h5_b~}�Mǣ��f9�����H����{���l~;��V�jn�.����4�ն��,�;�l�3z�/��1��d��N�߶���Sk����N���Ǉ�#jd䪢HSb	i���k�T� �s�hA�n��Q�d��9Q��8���q��,�4!�V����K
��\BK� ,�bRm��N#�~��l�X�
�lA+&r�8m(g�\��/C�iV7�^H�b\��4�A���9�(w��\�����6�i������)++s%��3xD�.ߺ�s3o�f�??y?9���m-���[Qhj�b��v��z;�p�`�ak��>g�>�?�9�6���8�%I� P���I����E���Md�U��bS� ����
��?t;V%զ3nu3-w+p��y�b9�\F�3tY���'[EF>�rM�]</��|����&�AE<��]�EI�����7�H�����n�z�F�b�p�0bZE���� B��M,/��	���G���L���|o�n��-�䪢8�}'�z�܂���K�-�����za�:��l���6]E�l��,ߡ�3&�.mL�
���d5ƭ���U�_�E7� l���y5�do�6�(l)6 ��s��_t��7���fh�s[�h;�G�_8ݲ:��cX�/A��}9���jD\�'Z�3�� ���C2�H�ʖ7T�P`]ֺ^܌ÄЎ9]Q��gi�5+ TR@�,��	���l�1@����\E�na+�L�5�2���uLй�M[-��IpST*�A���T.��%V8=�<p��a��=a�W���}����m��5p��s��$�>�Ƴ,~O�4��;�0K���虹x�����_��{�����wͫ��G��C�0C�0�^�e���Y7��A�{i���6��M/�9I����6�X�4�Q��N���$�T(�'V(�Y��ӽJ�#%�,K�*38J'���Q�dϫP�vθiP(^�B���ƥP�/�P�1��B1��=`��!`��!`x��M�/CTRjj��@���U�bp������cR!ƀa�JH�$J�g�ڇ��9��x
�K'G��x�����3���z�W%��q����w̫ �d	��!`��!`���a{B�s&���%����~e,��>৐�[/�I�y�&g�3l8^����DlКb����Q�kd�{����%�+�v[��
g�%�����4���+�|�jc�������7}m���q�y M�q|���Z���dA_{U�ھ���v����]�*�k#�_��!`��!`������zK�.�n��Ng��򿐲��$)��ռ�pv�ƽ�_�
T$Lg��Q��G����ٱo���!bd�1+�ܘ�/u�]Q_���C-jp�S����%M_�s�U�@��3�}v�o>u���p���X>�l9-pˍa�`y���8b�TX]z�+�'�]'�o%��PK��$[  pY  PK  �@�U               word/media/image1.png̻eT�Ͷ�K��Kpww$�Cp��	������ww�<$�k��Ҹu��Z{��{�;���g���%����s��U�������������)b=ڟ_��Q�	{T���N�1���{e`��ޡ˙i���)�()��)�U,ϖ9�	�j�	�x���^oZzxy��h�2;�9|�{I����:ڇɚ[H��?� #�:�����*ԗ�|"�Az2p�{�jOl_�����n Ϻ&O	�N�(��M�&~�EN逨;g�D�&��1�h�f��R�1��ʪ�(B&!��cg��Y����k1>���
L���nي�1�2�Y;v���_�"�}P�@{�nd�n���=(���=t����;eZ�4�d7ͺ�Z�%���*�B#EW�Ah�!	���eԔozٗ����b�R���A0cD��E�B'7��q��.J�QY����崷��G|8��4�
㉑�+��˧�Ra�1���qz�e�$2�V�����I���Ơ�h�'`2�9���Ǚ�k`9ǵ8�������k�wWB��,Pj�s+r��ɫjvb�����|"(�M	��7��1�����Usw�W�Vm�(K�a��^�o�S��Hj�Yx��?�P�M�ܯ�nG�)~��+���[��+V��i<��[[}#���S�%�����G��1��-�6���j��R�j��ލ!�U�pA!���I�O�ݽ���He-��g1�E
6}#�dg �h)
J.mL�8��֦�0�Z<h�?܃CGO�������t�������)�EL���$AW[A�5б�9n�҆+��IFr��p�i��]��s�`7
����rIO��Bt�"r���n�Y.�0'�u�ӑ��*:t(��"���
�L�����#�q��o�]���G��c-�y쁸��1�Q]�X=�,tcO�
����ީ�ZV�GEAFm۩�g�k*G��{ ��&�%��
P������ϑG�2��):!+�|���1�j�`���F0������H*I�g:a�~�"�� c'��A�mT<x���Ȭ+8���)��!�S��NX���^�a緬�#�c�4s �,��W������/��G��}��7��"�1}����+�]m�i�h����C
�+`lEh|��pK��DÉ��	Ø��0ULG�O�]ϭ�x}�l����H��[��7�{�����������[e��CWG������BDw��=/�F��	�.�����YWK��f���s����VB�i�<�BO��q��u��� ,S�>��2r!�Qn#�W6qV,
����Q��e��^l%2QUјI��m��x���b@ݣQp��|���Ay���5�����T⻀�ڣ��Pa����������Nmjh���b��(��!�%�S(��$�#� �S�n���'�Sl���D�ZB�a�0��u��G�k���5E,aP2H(!&��Մ���3���.7-$���/=\�}@��yr�u�*�	���9��O�J1����:�0=Å����=�;h.k��^F�J����="�NN���j�z���1�2*��"�D�n���Ɍ?{�ɐ&��o:E��`>*����Ȣ�4o:X���$����ĵ��ɤ�Q'���v۟�N�� Y���j�^@��8�<H���4٘bÀ
Z���8�Ћ�c���qU����>��s���9~i�mp�,*/�+b��+Q&�"O�� �.���O�&�CO=ob�)ǩ�Ć�όŔ`����(�[�o��]�-��v6��1���j�HBC�ܲ�d�j�,"؉P�n����HDXG⻬~D8J/2Wcr��9yx���v8�ݺ��N G̴���~��@<e��5`�e�	Y"�&��-q����R`��w	�Q����HF}d�P��=9���s�Z˗;�.ҙ�A�f������x��Ƌ4ci3��rG��8^F(S쏽pң߷����C=���q��Z*�YH���z{7����H�g��B��/��\�M�F�]r�xX�O�T����2�n~2%�2�8��G���̼�����e����g��E�hT�й�N%���@.��`u�sb�w���MZ7�CHc.E6�:��/m#|��)��V{��u��t{���ɭ�A�+S1��5�98�o��	M�j8Ng�� �r�^d�'���4���>�`�i輳ӬR��eF��Bߝp~�k��kxz��;�4c;�g��Ҋ�'���8�*��� W��a Y�Q���}����^�-��l<;Ai���#�yS�N�rT)��Pv�,�b} ��oV�̒��'��zY<!�~��:���K �{��V]j�
��0L|5�ﲊ���>o���b�j�D*u��=�v���!���>J{z������Ĳ�[~�7?0Bn�e�8���%tۢᛲ�ZvAJȊZ(E�����u��˟%v���k{�� �h�O��I�S��H�˸�Bq������+`��,�8$f�tT�I��1TGG
+sN7��w
�k�Iț��q�k^hU�a#tZD��!H��,�)u�q�v������fȞ7�)<+�JCt�ۜ��g'A9��,tS�d��ph�D*:�y_�!���G\z�Ɉ�W�{т*��es.��E��	�^�rp�t���sȌ<�2�~@^����.����4���F�y0�1��v���!�����(�±�Oߚ@2�,�^�Hz\�ǋ�r`��c��/B�Oe���Re2N��G����.�5&(��p$�ra�Z���x�����������v�g� t�K��n�σh/��뱎;�n�(�{��)�*��i�W�X�����E�������vgᦙ��֩IB_(�^�!�e�W�'�䝋!��+Ȅ��6�):�C����u޵�߸s���5\>�]��DT�����G���6?&y[D������3Љy�k�3������[�?���A#;h~'2�GZ5�Z��-�� m�nԐs<��McO8l6�^[@`�3~	���Mj<�$���Ȍ����1W�z��C�y���8E���cm=�V���P��6۬߮<��j��۲i^�'I�N�����r��e�G���4���D�S	�'���HGl��H��S�p�St�`���i��Ly|���% .x�۪\4bWw\�L�{8�p�����R̅:�<"=ն�f��}�뗾�_�|�d�b������ �����1�(���� ���K�rl^��ǻ.ꦘ���Y�83>;�3l�U[��o�9ђ�5}glQq������w�}�@cL%���f4���Q�$�BZ�ӜO��G��&	"6���,\8�B21�!��t��:���M[��)�ò� ٳ���c�`�)��yn�K�1t�+��jm�����Ŕ~x�֢ݎ.�O�-�l)�3��?-�3P_M�n�:��Mט{8>��Ʌv��]�v$}`B�Ar��^�C��z{'h���)��3l�(Hn+:����5�
�~�j�l�-�Oţ��f�;�]����Y�	K8I�I�ȃ��S�����T�Y*�|�q����A��`�6>P���{ɂ��NU�0�Al�w��@e!�RnxF��H�	<�5
�����׶|BZ��=��hf膩�M<��|h��V�Lg}B׳S0龄5K[>;�{�+��*��� Zm�O��Yh�v���R~���m�G��G�^� �~ӣE��$��m��n�O��K|�po�6�����E���,'�(ᰉRi�:0��kDLM+e��NJ-�W�K^��B|��En�<���yo��GJ�����#�h�y�������K9��|���m_y�B�fv�f��MW��ݽ��$�&j#jY�&��;7y�����`6��4�e��m�`�N���B��ݜ�M6Gٕ���D6���C�t.�v��8�$i��e�O��8ĵ�~6h��X���O����Ϯ�;�|��4X�-C���r+΁��#���;����צLh��Z��Z}5<qtS.|���a����Z3�Eo8.�3��I?�Wp[��;�`!���O{"��䦢��P2�=:b�QtS(đ��C/�����y�Y���ߡ�#���-V�5��SF���ْ�z3]�3������I_���s�M��8���
�����80���?�jH��YR��G/�<;׏�X��RbQ����MSWI�[�,�Oì���z�g���sK �		T�w�k��+���x,��JAT��.�$��{�t�; �r�j�B��c�b��>�WF���!a�,;uڻU�=�b����a�ϒ�����'��&u�N��t�����X�~0i�Ҹ�H��P�sE���P���.>�5�6�zSp��:#'Bl�(���i	O�����޲��WW����Dm���	<��+AbӾ���(��3��ڏ����x��J)�-E��]�ዾ��k�4տ=�6��~>���Д���_���7��b��[IgnG\JM��[c�ʬ]����%U&�=6�?iU�����.XKr6A�c:�:2*�g	D�+����a5��U���*����$1/{������ރ{D�e����ը�`g�k��O���b�d$@�?B���+f#�l�`����T��M�G�F7��8�#���8o���F.ij��������� �þ�uV��������zM}�^n.���rJB?D��=)��DA�t�jD<���n!&jN!�Ը�42�5Z��Ӑ�d1\ �����ϓ�dɸ��?�Kׯ�d�J�a0������ [֖��5t�,&X��j���*h���tN�
��փn�kFx;���b�E�����Fz�K�I
I	$|\D�q���L���?
��������ڵ~c��F�R:�#�i��a�j���q�����p#���'O/��Vf�z���;���;\�ֲ��ðN�-wl��v����i�P�|��JIf��@E�+���^&A��y���O�!���J�CV�� c�9{	$tԌo� Z}z�l�ջ�C
�R����/p\�}�7�3�<;�?A�St4��C-���%� �x�Xl�i%-�a��J k���GT��)l8�U�r�j��|�q�.�cIY���V�@T)VG�u���{ ��P��\�g\.�/\>�����?m���H$z�6q=��Ż'���JF�(x�=i�~X��y��C�����h<�b��n��nX����Rq���;ݵ���09����	�i�6Z��6��}��u��cP��S%��`07�0��W1Y�M�탡cC;&��R>r���nu����ڵ��V'�̺���|a^Cfm{��K����H�4�'����5�ss�)�kZ5��ou��'~wl��\"��j��0ٯ&���������6��-�G-���E��,��xn �(�YJ% �v�a�Hz� �� I^�f�%:�;����>�_���Xh-A�X��#�<�n���_�5ti�k����ҖU��f~�t�l�t<����T��8=��Ws�n*K��uZ�;r#əMm�lb�#B��jl�	#3�{����[����"��˻��4aR����z	�����?���d���K}��B!H�wŻ�����%ꩾ�ts�R�X�q������O�����Π��w��7}�#��=`�@�+u;E4�)�Ƙ��a�$��S���Pl�z�F��:� ����m��"~���w�l��/�GXB�}��f����i�l)b�; y#%�����k������_�95iT�&��S�{�K6��j(�$�����p��ɶ����t4�@Ϻe�;�_����Y���;�I_,'�^���KE�~ߧGwC���;���]�R�se/6i!V:��[�vfi�4,ƻ:>^�6j����ە�B�'?S/�;�w�A�3%yo/f�87,��E �Ӟ�~�yk�X���)o�}��z4h=�G3��|Ӣ����@�e#y�Z�z͕2C��Ie��c�\p��dʊ?�#�qʼ)�.��j6��fGb*���L*�cs�kY���S�5ӂfʥ�FG2��6$�Dg��<��u�;�6��pŃ�*[s������A��婚O]�Z�g�]!JJx��i�?�v͂�S ��A<7cl�HgY^P��� ���Mjq]���Y�3�df���*���!�#|>@�u\y�'Y$�N[�3�����R�2�Wŵ�R�˿T��k�����\��+���Q�h������<0��j�}�R�=g���������(���������?�� ����"t�p,Z
����[0��4���xGl>�͂w&a)4��!�'ܵ�n��ۛ��I����]��X�@��;8U��e�����S���z�Z@pI%�-]�9�ק�-1��
�
�Y��<%�
��>�b�����xț&�����Ѷ}����O�w��5�ytQ`,� K��JP�b�1}�T��#D��HH�֖ۼ.�Tkq����$�o+���ێ�\����>�y� |5hy���-U��W���y(�� K{W(c��+����G��،]H��&=��!P�D�	i�6����Eb��vl�ǈ���|;�,:J����1�ϪM� ��pO����9�V����|�e��^N,��0ʤM���dN�}_[���Y��'�ئ��މ�K�!t8�v��oJ����Ӷ^�����o��̑z���GZ��J-�S�g��祬��}>�@*�6��*�Mʂ��@��l���Z���<���*]b)P��M�HH_k��;��M[O�9��`��e��YAi�Fz?9�_t
�m\J1�P&18�oYd��G��i[��N-y�'*=��e���l��@̎�I�$P�0K^�Y�Z�$r@Znr��Wsg�.3��^���t�"�v��-
�Z��tn��9'�x�fn=0���pio�X��Xpl7���s�[�->�3�Z�@s��v>�����J�E��v_�f��%,�ZL7R�-�w�?��� k�x��������}�I�BPPЅ�A��6xSK���-���<�v�
0��R�D<��^�N߭E,���!j)򹵸�������"�l��#8�6�,�M�/F`��Og`6n�k ��}��4$s���|�,SL�'�~�UhϣWN�m��Z��K�.>��m��T����c�À�������ʼ��V̂�.�9��:�^ �p�K�oYD����l��ϒ�� ����E����o�����ɛ ��ց�"͛��rI��?pm�8���J8�3��/�)�L�J���f��"+�c9�����{�k������d(���S�V�Xq�����iOUmKdM�ٶ�c�E�mp`n�Bx��Ab�nJ��X3��J�,�R"&$^�Ea�Q�p.>dk��2 4]Ơ�h�}��'��4h�U_�꿟sRͻ���m�p�1pjdQ�G�{����C���`<������K�2k:q�[?��(��p�!	�I�Gp����{�F��Mͦ�Ƿeܚ6��o���Ze|��y~ʜ��^o�G��&k-,gUH�c�ޅY�R#�4Y��^"ކ��lj���V��Yp�@�y,� �^�rMDQ�9w+o��;K9>�eM�t><�OڐM�y��N�ܥ�T�]�$k:?**BǞ��9�З�Aw,����	X`�X��sS�� ��-Q^� �Ao�d�/�S;���H!�p���CxK���m���1��_1_4W���>�R�>>з�sz�X5�p��7Zb����Ԣ\����G�XuD��
����R�W2�O��3���o�sw�|=)Q6+Rzo���ŭk9�a�7��M8�j�x�S������9��֌�b}� T �Ć�wK�F9.1���`O����^N��M�$+~Yٷ���fc
H�D���l�lES���� e;����l����vޒ*z�I`�P{gP��v����Y̰%c"7T�[=P㕞����%@�e�ʦ�2R���|��e$U�p�Zu 4�|�:���~+U�^^����{D�K��T����(�iw��)3��ֶ?��yzX�Rέ[�;O��n���RC��f� ��z�aH���8nv���HOo����DXvH��w��6���F��g]�ޮY|v���F�>�L�� cK4f�>2���fX��C2^�R�A���,A#���*+��`�b`.��3	4�&+��X����v�m�ל�s�0\m'L�Q=r�戜&�� ��+�Ձs����܉���dY�vX�T)w���qY�W�K�����yE�IQD6�n��ؐ[���m3�g�Fj��І�Y΃�,PW�R�\��5��+J�U����ʐµ1>$22��w�6��2��;J���諾����s���"\ȹe�_*�I������S��{d&�(�ê}��A6՚�1�����2���Ю���� ���KO�ME!h��� �l�K+�F��e��8u�-���1Oķ1i$���-�>*Y?<�y� d�?d�$����.M�4�H�Җ�iOX���M�6k���C����I$�^���c[ ���crG,����q��}�E�*	�%�����;�du%��r��Ya�����ϯv՝��l7;R9�*Y^���)�h���f�&E���i�N�S�I)��E9�������t�+� 0CH�Oc��n��|����@]�ٲ�ΐ���\dy��h������u&|\ ����j������9��=Y�}��	C,�&��[��~l�M���LT�<���wz1��$��R/:�l�i3������'L����ٻ[Ke����.ڎlȶ��d�
�b�ﭲC5��6>�f���_�U����I��TJY�N�ܤ���̹���L��0�$+Q4��вT9!i���0=ѻ3�N4���i�N�h/��f���{<��kJ��y�����?�����S`�/�usYW������B�^C��$��͇�d�F�f}���o�,���w��E�|.����}�I><��u��G
M{Itn��h��ݓչSx�/��{�����w2ZZ�a`���;b�y]W����mc��%�1'��Y�Xfm�w�?�U;�8`�6QZ'��w�Ǌ!��M���L��'B��=x���m�j_&@DC��?�.�.�;'8e1,@����"�h�F�t�?�?v�ǅM1�<�r۠-����2ʫ��u��������P����k�8X����>t -Y�k�$m!O�D�	Xq}_:�}��y"�G�vS�#Y�Xz������30��Jd|x�'\���DK6û��C]	H�q��V>�K�/Pܳ/s"F�r�`{�W��F?�w�����t?�J����86\���w�����{��;�9p�۴����(qM����ϓ�?���Utck���I\����d*VǼ� ��Ŝ�	�X��*���X��<��K�ަD�]��}�s�9����i�Y�9����xC�gp�k��B��o6���`�PUmЂ�D̔������I �Y`	F%��h�e�v�Z�c�_�k��Yz�J�b�u�G�T]�{�Q�!,SZ�����n���v�-��b�Ih�A�1�hu7g�_��P����7D�N�$�l���8��ÑR�z\Ʃ�j+�tR���D|���|��4��-������e�\�W��&F����~O�wS�#W�����O/��p|P8�3NG�o7,(���/}g?OiY���Y8�?R�A�*&˳3�H�N��iS���e�x��sh�\�h����P~���ݎ���֪��E�E�5��ȼŽu/`���4�B�WW��ק�A��cC��po�<�xX������+{���˼{TM�M�S:�C��Ը�I����!,�n����/��"cK��@��,j��_��8�����s;Xd�o��O�!T�O�R��fX�AW����Nh���ㆊ5�,< I�S|�u�����m��Ze��
�L^;�VϢ\���AR(�UchD@�}-�gxFE�Ҷly�Vķ|�oq~(��x�S���!����ܙn҈�1}P��/�#i�k%B����U���?�S��%��:���}��|(QJ��y�l�U;�v�zk�J�
nkh]��Y%�͎��/�,�Vկc�a]�Q�������F}��U��R�����I���p�s��2:Ǯ ⪹�!حèB���C��3�p�9M<u�J��A��
��I>��̳\���ge9}?�P�VL�FLbd+�r�Go�;�7y��0�l�%�w�y��T��t��G�FW���Ng�n���< α�{���	�H2�CPZ���
0;b'-`M�/��R4��朐�[z^o[�����U/xt����oi��\]
WܹQ��_s��M ��Y?�+��MC�赺�9'ݾڟ{�<->�i�n���k�aW5�m|��%����"L/LM"*�I��U��9=4� �>޽�,���!3�\��V���}�u���j����&��?�8!K�}6�����	Å :�| �S������� ��$q �S� 
J��S����)�&����+��I���h9��X�v~#4�<'�<~O�>GAk{'��5�G�J��+Ўԇ��� v�/&X2�(�7hۀ1�;Y��s��+r�	���Fa�4qs�9.��F�9�͗�)P�u�A5��X�fh�t�1׳j;Z%7����t��8\���s�����4���-����s�9΢ė��9�feau%ҵ+øHCpڹ�/�4ꗸ���r#�$dK:����B���1�/	��@���XĢ��jہ��&��
��tKY)e�][CJ۲8^�x��ڎK+��3�uǧ'ǁGZ�`7����
5�ΰf2�1t�|zj;zC�v��XΟ˅��na�?Rqe�i��L��X�2�n7~#�\_r���H=k�a��;&p56����ׄ����^'��c�^{��Yؗ�#�_�N�1����i��2��xK[C׊��1����ӃS~e5'5*@��^�y��~fЛ�
#u��t���tYH�nB�f4�5�[�i�zbњ�d���y� r��܇�P�T6O���7_��o��?�cU�'Yb�}����~��-�
0e'��{�,[����!hV��Q���D�n�NcG��s���USF��2�����OU"�i�?u��7t{M�������&N��RTh 2���mV�?�)�':�?v���h�o�U[�H}X�wDGm?�6���kʭ��P�L_G���fѦs:�Փ��9���#���P���sz%�D6����N�@�#��z���XYkn�syV�d9о�܎����H�U��O2|�ŭ�X�ظ%�A�f/�N(ǚ*�4���P��T�7_�zCP����	���O�Xk��@�L��m�D�}��V��u~�k�m�[�7�0�C&�ًgZ'I؉��nV�[�������/m8Y�ix���O���Z�j5�$�)�O%�*�&��Thp.�������w9���0�����Re�;�QѤzj�w_$[���%a����_#�iݬY�ZH���)���5xѪ$
���'I�B�2ՙ]b�#��w���a\0���Rm�7��Ɣ�]$�RkG�V8t�blb�!�K~�YR&=�W--qp�t<�9F��M����X������@4�I����<[�YVk��ۑ1;�_�:b��� �oo�sG�|��7H�#>��U�T�r�
�&�Z}�)��y	PB|�nޣ�$�9�#�t����J����WQ������,���dJ��<ukx���.�1�!������0���k�z�|�&�b\Ql|7��wx�~����K5�Dp�{�-���0*L-�0�c���� H�Y��◃7HykL6H3��H��)�� ����i�� �M�F�`���g�d�<��G��?_�J�!n57�xQ��I"���Y~q���^WH�!w3�3��m'�-�m�z₉�'���a�K�%��s�3-����+�;�I��g�5��(��rY�X{
�x��yo.���OA�ώ��Y��|YSz�k) G����(mWe���U,1y��kڈ���B<|ǔ��jD����r�T@��)��)$-�� ��n���qz�����G�)��.�t�a��q0-7�I z&zRX}{d�x��8G�(lbŻ��p-ڛ��9m���ty��;���=���>�8�@T4y�[�����s���đ����H����P9�L�v�,D����sS7٪��7;�ҜQk�6�ggpD2��lG8�;$�'�Lx�a������O/�-�qݏ�;���왵8�|�&��P;;�ly6�%�@㠼��o�:�?3�0�quvQ�n���f����֚Id}��Y�`�����玚;w�u�$���wBS��aJ��|��q�n\��Q;���ܨ��'��x�Er��:	�#^T�+î��;�\�u��/IS���F�0���RQ&���o������SS|ݫ*��,�a�����[-��[��r�\'�����8��U4_�V����j#�i�pw#4 �ڻ_���)���W�<,�L,�6Ӄ����6Bj�8�VC�SL��)4
5l2y{r"�������X�E�^�U�p��1�Icv-�@�;���jdï�Ǎ�\���J�uf'�\�0�gm[���?��[8�dMԴ�Yd�D�P8�_���6���aN���Sf����?'40V��kh�����w�.m�h���x��� n�E:o0�M@����	���Ǹ31>Z*���۠B�msK�X���I\���O3�V����2�Fan$@�+�P]��H�o��̀?�d+���n-���Ǯ����$�T�������k砞�����1|�)��m���mJ� n�'�n�p|���\�?6zT�z��!ĥ�ٽ���IN=�HΙ1��(u�^�&mֽ6�T���ii
5+���=\�V)����v_��\��(2W9�w��̚�:k��R�j�BC;�)�$,t��	���y[D�t�P$��c���R�O���7_`r���1utu��=�\�oJ��Bt�Yp��E�im�wj�w��md��ʌ�]���c��Ex���C0n9������z����X~��ux�
3Z�8�r��8�2����Y�������&��LZZ��Rղ���\r߭�r��3^��Z����"ݶ>�V|=L�
&9#N���99��QȄ����)gU�|	ƾ���Ѐ��_+2�C���_��t��
X��xM���U]�N`V^?�|�&��3��i��j��o>�(��0�"e֓0%�u ;�riŢ�M�6�=z�1�®9_�s�9}|����ZH���p��RnM�� ޏ1/�W�^B<����bq�]}Y�4a�G�p��Z�����+ ��w��H�@_�{�����1	5���_"nme��+Y�t��p�7�I}�t�t�n�۹JN.��ޯ�$߽z��$��Ɵ��yz7�D'��1�д��!����N��ѡK��\:Rr���dAKD(|����/r �� ꖕ��7W��nٖ�P�a��B�'{��0�[з_e�
��|�}kIPe/m����7<S5`Ty��A%"\��:;����ѓ��:=�;�94v�=��k���x�[dFU-�#���:����m�_=&�8��Ct�g�D�����x���E�T�Qo_=&u�nv? l2��}���wB�!�e�Io��C���{����-����_F�XgϞ�j;�c.G�HD,������KE?�%L�X�'��ĭ��z=�>B_H{��XR���r���ZU������qY��Yl]Ƴł�s�#W^#�z��E�� F��5v�g.Vu�yl��������}b�͍:5;No<��Z�mX��r�ma��	ڂ3��p��B�wW|sL��?>�|��˗b�u�V��v��.;�Nϋ7YWAW��ނ)��G�̦\t�#R�k��ʅC`TW�ct%�Ͽ����n&S�M߀�O���}
�ōeTl#�@:�R���>DtE��g����χJ'<��ikf�=/o0.�����S[%��W�6�zw���>�^J�8��e�m㸚P��mp{�0��$��jgi�.�x$Ie���q��?p .2d�C���,������d�~t�˸�y�23F҄�/�玞�i~G��`B�uQl����H��g�
��[f��׳���w��U�^���m��s��svɈ�W���Ğ�">�\�`(�@*I����ڃw��r��p1C�y�P|y�aΣ�M%�}V1I�����~%+!3\ᾣ��A���a�?�֥��2�3)�V�����ãB�a����`JOs4�sʗ���>Tx��ۥ퉋Y[ϱ�X�x�O�֢�*�Ñ��}Ez���8;���/&q�v�r��~��->gX_.\���u���6LJޭ� )��ŉ���Լ>����ZA���>Lņ7d�d��I�gα�·�Ϭ���By�	,�&�
*yv��D���5��H�S�W,���񈹌o�vL�&L+�/MV�:"�)�3d���J�W]�1V�p��z�*jJ�������\�^a�'&k=�h��6��W�ƈ:IgJ�^b]��[	K1��sԒ_�(��f�Hw]��7�o;jzI]䥦R��V�hd�՛:�x��ƀ��`�#����gy��p������C�_�d�}���'f`���~���YF�A�;��2l~�<��`���7���['mK��ɱ�)��hڦ�^�V��
�R([�]�P$�F%�(���ޝ�p�~�3�J4�	��@z!��j}v!����>A4��\#�-����(�2%�G���PO�T�g���?�mw��<o^\f���|\��kA����I���^�U��]�=�vջ���|Ԯ����t"2ե��.+e�&?�(^�������#�W�����l�!�*`���.��ەڔ�JT��w��8ҵL.����J�T�4���s������b_�1o7���}��ɪBd��n[F�2�gM�_�	%8���!U�I�G�2�p!�a��������d(��ߪ��N���<���wNnKa�m�e���<B8�ψ���4��]��<�C���?	@ɎuLp����'�nh؊��R�v�'��H�sË��
�,!���WVg�~��ƶ���~�yq������s�h6��/�HR���{p�yvjS}^h��TFY����Aw�X�Ҏ�����P��_"t�8!�2Q�S`����x5M'�����xޏ|)��q��/(���(��@nj�7-�	�l��cN��<�# S���Cu�������
���lCmEړ/K=t w����\�x/��ś�'�`u,�wa��Ω#�kwsF��Ÿ�#�I�f��f5y"8:��6B�$�%2���iaϷ��أ��˧��(����Cޞ	t37��mR:�0��Ƀ���y<�[C�Uns�Ni;��A�� �#��M�T�1W��Q��XQ�-��QÏ���/ڳ�ݳ	�c���Uſ���2�;�h�\f������dl�S��#'O�Axj,x�6���ۭrƷ�@�Ⱥ`��Ӷ>�"��=��s���6���%D����G�7p�\�̄=.����QV �x�����A�d~ʙ���-�)k?�8|K'����2a�iɘ�Ա�I;p�D�p����7����k��*��u���I�l��M�:����hD��6�s�f��Y(AF+Ե�����ƞƧ�:�/k*�<����sxX!��&�ً�&Լ�h<1�n���W�8*d)��̅���u!(���<euMj0+�*%�$*�Z�w@+1ኺ��4�$p�Y؊�ό��I�^��a��!����Ϩ��̧���%�z���ϴ�
���l�l�4*��ˑ������7(`�Ӡ ��y�B:
��zT� ���1�(Q��v�ɛ����YQ��~��)ҋ�o$�W�i�>�b�p�	�_�zy�-ōN�dl��#K+b�t��$�	d�'�)�8���&�ĖM�1�\���F|���c�����1�N�{E�>�#�R��(e$k��:�Іd�i�0$f�s�k� �(@������^��Lk*� "Bk�"��\�/T�E��rg-x�:��>��῎�-� ���*R@	�HEz/����6���O�x�����+���VK0'��1V�Dm����'1�2������l��	�=W׵*=K��q3�a�})k��l%4��OI �q'�3�0���hz�89���֖�y�N	^w�e���"�U�:O����m^'�HQ���u�;W��G���5r��5m��]X���g��q����b�-��̖F�4�{pw� A����;t��;�Cpwwww	n�i��L23������:?�������֪��"��*-m�PI�)>;�mk�̠v�b�s,a����1 q�v�����]GZ5�Y~�O�0���	^vz��h���O(!#=�!Y^A7,�|��n`���H��g!�^�n�]y�)��V�P�����_��U�~�\����-�����1�"�d��+���]P�Xg���}�O��&R��!��+ۮ��*��$𔖗�S������R�@��rN�-e�إ���,K�'.�*�3P�PWy�6�L�����mUQ���726Ĩ�`�	U�-ݖ�3!�N1�d1�'�7b?u��� j"�t�
�W�����U?�kO�QB�'c����j*7����O��TDG􆼆P�8uo�%ך�A�9j��٥力����:R�Eu�Ҍ�X'k��띫�7DM~��3*6��[�4>^��E���4�6�NE	�ɭ�i��-���daSR���=b���"�n��CA��(=���G!�?P��G�����ggc۸O�4RӟܷxQk�si���$E��|�`�w��?���V1���Iֶz���e���F��|�$,C9��S?��6��B��ؘ9���Wc���;qS�SDO��$m��r���OP�ޚ}�0�D�G�ޅuցVSK�'urճ�X����_!�>O�Rh���t��k�j�u���b_�XI���?���&�v=�������'�����<�k��?7?�G����GY�x���� �+27
e	)�v���%E�կؼz��Bˠ�b�gI�U�+�<���F�ٴ�pNa�{�ƴ�F�{��h����!�H�zV3c�!�@�f��C�I��Kk�-ق�(�+ڳ�������I���+���T�f����/[ePF|Ɍ��hL�t�N���U����)XE���,<��8j-"��d�����������XZX�,,�(���q�f�By��qA9�Zdd��z�Ч:��-0親�KE�g�OU)gNP��_Zi}m�]*�ls�Ӗ�̭���A6�Hٌ���K�����'��	;�!��tB	v�an�v� 
����`U}žw�j���?�����:s���5�-�����dH�	�_v�-IIS�h;V!+5bL: `BXZ�J��Vbl��կG��}TC����S���p���*+������YΘsN�7D�Z��s���_��
�-Nާ[Ml���h�"#��Z��)E�K4Rj~e���U�uX����%体���Ykt�ߓT�Y�Y��̡����zɌGj?�&����r.��t��Q)�b:����b�񫈐���3�����}�K%�5.�H�R�v߉�6m�脿�ߺ�kcd#��� �2�Q�Y��/���ɯJ�c��Eu�5�ŧ��n��d������2��!s��	�̒v�jƧ���ĕxL�r-o�z�o�E����C~ǲ?�G������	R>�������d�S�nP7��������L���2�$5�He�L��p�%��4�l�aS�k�&�d��>�*1<��B�����B2h@��J=�7�y���{��j�V�5:���p%��m��i���
)�ģ0�mg��t��������g66��H�Y-؃w6�5�~�\��+Q֨���sF*�}��m��k����n��w/��fN�F�
�J�B/H��ja��+߿����ތ"r����$�/-���Bj��8���� 7M"�'zp�^�S}�#�b���hk����6�T�nC�٥���/;���u�t�B����b��#�����ǂJA�V�����#�������S�>���$"��[��ޖ<��c n�zWq���;ZK�2�^�OlPO�������dMV#��JI���?O���L������������a��G��N�d`n�Ȏ���:��A�D��0�1d\�o`�*��'C��վY�GA)�e�5I�`�h��Q��� �Αl����_��E�%�䳁����;y�o|^Ezu9$&H�a���q�Xg�j�}�Y�ױ���,^�@��K�Q���d9ۚ�Q���j��!�"�[���d�����KN��w��p�V*>��?q�U�~�^	�l�-b�%۝e�#��ɐ�6��:m��]\�����,!���e6k�ӡ��W��-��-��M�q�Ɩ���U��9� �|��T�s΋�����̊s�0��+<�:N+�^S>��&���;����ͺu�°a+>X� #j�wЯ5���U�B?��?R�N��-ҙ�/|GM�%��r��̯�����F��b61;�G4՟h��'XL�{����K莲m�#r�x+�4f��D��c��.dN�$��r�����w��o�\\����쐡������&)�uw��n�9��?a>c�V�c����y�"i��1x��Z��p_*E�>�c��2��i�@��t���΄/��R�M`��|�P����]y�o����~��%1�L1L����G�X��Ԫ��V���g��A�p��{�63����-�zu��GR�[�n�n�ӂ����F�t/Vj�Ktu�\�QK�]��V≃�Hjy��tե���+�Ѝ� Ì�
�C�p�7~	K��̖��/�~w U뼃vm���д�5���[��&�gv� �����Q.���qo�$����Rx�&�i����<kt[��&o�x�֘�9 �	���r��Ģ	���Ϛ�i����>�b?�j�$x��h��޾�z�(�5��.�;G��Z=@�"�6MA'.r&\��qq��-RQ� �4xnX���OGM�
���9��Z>b�f����w����on����J���~�z8qשx�po�ơ߽�t�i��Q�����]R�n���Irnob.�_�n���F�U�{�bjp���>���,y���<w�rm�%��z��A#p!� ���r	�\�]L�2"eY'U[�Y[�`��FH �Z_~�_�F�5!�{�٣���V2��QP�dT3�o����\5D�Z8x��y��
�q^�K�P���թ��07�^Ëq>�����z��ݺ�1���(H 7��(#�v�5n��аZ֌��N����!A"{��`W��-���S����!3X)�J��F�����VLiW��2������&�W@��k�/b6Dd�;0n�`}�N�0��·�,���8�K����_}�_C:��ٔ�>��7���o��f��1�bbn`� ���;���$���1����a�e1�u�_ƺmD���Цɧ%�8&^P�gُ"��jR��'˽�FD�*���*��qAꙸ�ik0hJ󚌑�/�_�I�$��ID"9�E��R;����U�Ϻ�D�,�1��X���x��-�xG��:I�F�)ӵ;��9HV5����D�p��0����^[�q���W�������.��:�H��o��wi6�>^�?�!�(.�z��+n�	W��H�Jk��޾��T]#
�?[��pi���A���&����;��Σ[���g�}$ity�-�$TH�\a�ڴ�Kl,�8���B�h�%	��^����H�+�E�A-�������jx�F��.�e�1N���Q�w�+��o-*��U*�>A#�sw��ul]��m�z�zH6�8��Ipa���d�i�p_��<�S{��#�L������%n��K1{�G�c��3��ǒ�������Kj�sf��ig����8�B�r<��V{!a�y	��9���(f|��n�C�W���+�KU��ۨ��7QJ��@�m�k/�E��f��3��^��92���;���^ ����A�Ì�=��]Z��Ō@ƶ�x)�g������]�HI���T�R�Y<��q��[�c��3Ҡbc[�COB�13��o��9��x��G�!UɓO#�Om$�O`˜�-��L؄��5>JDV0�ۙg����?%��6���^��u�>�ȗ�0*RBG�~���R���Q(_Ɍ_��؋�n�a����3�Y��I'����{S~�Ы���֍�t�7��O�����hl{#��T���R�?���B��Ahr������wy�N=��G�~O�~�lf�|�sh��ʍސ	����@��O���g��>�\~����w��g��;�Ch59]B^��mf��f~NV{U�9�4�$���o�
*x5�{N��u� � t��?s���f����ic���Zg�I�[LM�>�C���H�!pK��u�y ��G�Hq��v�%sj�
c��[�ip��9I�l�K~3{, ��^z��3�����e��L9��- {���CŖ+A��%&�/���H�٫\���+9�_����Q�~3]��N�T�;����#�q��4>L��y�)oTneE>�M(�qF
�N[U�[���V�g��<��������Zi'���t)�����4|ԕ�چ��2�V��LJ��X��'t�>�}b��k�"�H�lo.����`.��{ � w��7&�����9��/�9s�����ax;��%���u&Tx'�=A͙,w ��eQ�:S�����k��h߸�U��+��_�ym�ӭϋM��&j�d���"�U	��u��9J�lP�J��]Ɗ��m��O^a���+T�Gx� ��Ш84�>M�4�QS��UÖ&���wp�~�c�57we�V��%'%�\�jAf*&j�Ҏ�~5EC�9Jw	S��EFv\ܒ���Mm���W6��.E�o{�=k�L�eۏm�+�ͨy�z��&Wm��1i�����9��X�z��ξ;ٲ�mM6�̿t���<aF!8���H�M#o��w���St��+R�Rš:�\ �����z�H�X���A���a�ļ�i=U����y�p����/�r`��ǌ��z�E��6���'����vt�����"ۇ���k�R,�t�*�������S�Q���v��m�|����	���-7����}S��;�l�j��v7�5��y�4�m�;������3�%|L��Y��mB��1�pN���B�-��l�D��J�!�s��g����o�d���|� :��h`�ی}���{A9X�Ct��}����$.�.��)y.���%Qޚ<����{��>���
�>-MT�vaZs9f��R�%��N��m�^�ms�@�4�P��#�$�h#bϯ�L��jH��R���4A�-���~����5�햚��D�Wғ;�$����S�3�U�~�(ɕRi���6Ԥ��dp���,q��f����H��}!��ms-�����AB���;���6���7��G�N����넧L�^j2���@�����V�Ī����I-��=K�,T��7.�a��G�/M�O򩻺�:D��T�ǯ%<,(�\�5���Y4���O��H�W=���t�h�M?p���l���rWέ�Ξ�N@�%l5� ��2�����jM.�%��)��HH)��]Ȅ3ة$�^9�!}���N+���oh%�������MPF���`5��y=�@L�Ȍ�����c��hOC���v���&�X��RXB�N.�dC{Z�����I���
��e�i#�ڢ޵��]|�l\lƎ�u	����N�@�'i��Ć��BbA��r��g�
�}3����ڇ�U���%����֗���?6<��틡)��>��:
F���5̓���p/"�O�ۏ'���u��-�"�VS�_�ru����Iƪk�rJ$�O��� ��P�X��8�p���QO�%�}�����(c3��Q�[A�X���h�8П��wo쀈�L�,L(�!��(�&��ku"�HR��:��k����f�\��`N���TI�*�ϖ|���S��/�*.�{�L���KSf��D��mJ�,"?��VSZE"n0h>d	��W�;ĖžBIf �V�y�Q�W�Ă�D5W��%͗��x�>�����ٕ��t��$H����������@o>p)Ku�<4㫀`��Ut�:�}\�X%R*[�n�7����Ȉ�ƈ[�9{�Tc�s�!mg�����ǡe7))�s�@�}�>Y��wrի�eKe}0�>,��ܷ8:�W��[ac�m�dܖ�2潏�K�]2�b�/���g���>�)¯.���lv_���,M��Y�c����J�\�)��Y��~A
�Y�'��i��ܚ�23��2�Q>1~ �D����nZ��J�%���p���.*}w�� �!!���:�7v�Z�Z�"��ZȤuۖ�qnm��D��w5g��1�Kx���0��s�Ϳ��nS��+��fZ_#v=4�ڳ�dn�ra����N�沭�X���R�s<�oDhaM��*�m�e;����V�hx�M0x&�\	8v�� M��i��㢁�ɴ������� ���]+須���pʊ�G��?{U>K��I�Q�8\:���w(���������U\�8`�J��'��#�:X8�"�Yɴl�v���=HL͉U7� �u��S����~ڑ�e�O����8ha��953"3��ճ��W*|,�����r]�8��Ѩ��*�r�V�wcÉ������\o�.4�@���3sZx��,2m0.�n'xz�:�v��Ώ��}����it�g���t[u��1�|���ߞ����?F<��[�h��Z���%pt勦t�~���C�@�+`~W i:����-���B�zIR)tgb����c����Z���3�Jp@ϩ�	�P�^+�2����ӻ���  T�gA˙��&��{T�����cU�Ta\��[ Z�����\���A�O���Ӟ�h���A��ɶ�5�zes�xN,�z�u�lG:�������]c�/DRl�|�:��d&6�*�7��I��.�?���k�8�nU����(Ne{��f���Y2��/ْ�?>�0~�^��_V]\�&{�9�c�0����8��?4k<�#�'4W6��8����H���8������d���l� IH��}A�V�q���U5H�
���捿����	뀎�+��r�H��A9�(0��M���5���O[���U�r�� ����=��"������
�㛻*��тe�N��q�;����4���'2���_��L0'��� BJ�%��O��Rc�j;�Y�_b%��b巋_V�B�8���7���-�aaǮ�/���ډ��GGz��4S��?-d|���{�E�g�WK�;�(!����^j�aL�j�!���V�[���l��ҏ^�u��y�ݬ��3dv�e�����j��z�m>&�����?����q�)�'nu��h��Q7������ܴ��M+����$�g��nט�3G���c.�>�h]�M).�xMk��'Hh��cV��ѝ�A�>�s��/gޮ��6;�OLx&?c��\�O�/c4�rzk���@G�F�µ��N��5/b�j_����!M��%���Ļ�['�<�vGx[-�OԺ�?Vob�لq8��Њ'0*�2"1FY^��|�'�)��H}�>՛
��`W�PjT�Y�zR���R�!r�GR���XuRg��F#��Ӻ�����/�v�j�,M&eS'�+��.��~GU?ȣ�����@��[���qOG��⹊4f9�'/���oT�����ل惼!6ZH_*����mz{6t� 	���3}7Y�����G���֝6d�����mHz�zu=>���/�T�5�- &�%wh��u'3���^�f݈E��7<vit��.ƈ����R��i���(0�P���Tl��PH��S�{�����,�&���g瑓�L	�s4�wl�2�7�6o�gmg���w7ŋ�ɽ�Y�1�t�+N�H( '��6y���w�_��O��Y�U�TړE*t�����|������7)3�RV�
Ʒ���aj9��]�A�v�N����cQ���vBQ3�������o���y��n6�*��}&ם�sx(�]�vA#�:}��v�n#�s��^�ǉh�ki��B�9~4�$��Q��k ��
mh�~�#��;)��}����wk W�f�4W���㹆� ۯMo �D ����k>|��c�v~W�`���<�'D^�~�._c[.�s��B��nYII9c� 8����v��_Z�����@T��qL�����t�h����^��YS��%�G�1��8��U�*�{2.aìI��2�<��J^��]۷9Bص�a��W�O�9��ī�%��H�"�|^z����f �j%\8Hba�z�ЩW�MAO ����T��yP��k	R	FJ(�� �^g\�P�D���ArxD9h|>��܍j�邶=MQg2J!�fDa�&!���y�&���$/��4/�W��b��g	p��
[���{SuV�?@�C|f��\?�\���)��MX�M���-�Ɔ�z�$�:q���{i1Iy#��'�/��|5ɼ4t%z�5�^�q�m${��0���K�����C�bܒ��yE�FY������ydC��c�)+��4_ıŇM��-uCbO}|��!���;�(��
�e�O^Y(�{e��>\�u�?.�^�z�O�*�>���:��1T�>y�ĩ�[V��k�r{�s���6�cz��!�RI��
�)�8֡��:�?���	�v>{����s�-{,�^dp��MԎ�e#E��|^�p��e�W������z�z.��X���;F}�(\��P�_i'��>�|�L�x[�N�'��}IS*�w��ۄ
��)�}�tA���gG��z
�R#�8��@Ή�r�ˠ�J2/�]~za��U��`����_��~���kL�Y��Q6+���yp}��`���j�bMĞ�����}���}f1�K��O��6$I�Jz ���J[Q��5�vB���2'�c����T�_��RНȕ.w���Y�y�I���U��)!8o�;H���ޜ��&�ė���������*/D���ge��EX�4_ו�>����Prsu)��g7�+�!�iY'�����n��*d-�C���ut�	i(ή�m�u�^&֋*��B+64��lpk���hB�aM����Ҙ5�Q���6�e����� �pmN��}P3�w�{��.+BՇ��B��*Բ�
"q��G�Rڊ��ж���؇K^�5���ZեYGg�Gt�,!"$(2d��c+�1�!����n���!�x�d5�ڟp�2UN?�Ǌ���ݵ��'�j(]���!�+�W(�?6$��c�>ϖW�S�T��z�1���ݠ l�k�Hp%�� �m�Oq]>�|ol�w(O �hت��k3s�Uq���Dq�$l�D���k�h��;G�*�y��뒬|#!F��Zؿ�l�ڠ�u#,P\�Us�?&�!�pe���mA/5X�X������>�طfw�cml��F̭Fb��$��_v1Ǟ�&���JW�-�g��΀TV+_>��Rê�	��w�y:Z��3��l�_5 ���bV7��k���i�ήW��}�qg��J��q1��r׾�:`п�H.p�GAX��|�w��F}Tq<�t�����W4����W#����:n����4:+t��K��i4a�6:�vLpYWW�|7{"�yX\��d���� xg������l���r��"F۟�vQ桤i@�11[>@l\|�Iؘ�U����/�7�B��c�L�N%�(NrPo�=;�t	��4ntTkl�|�����4%��^�����8������wZ�)r�7z��K�4��ô����d��옿��6��`W~���~i�f�F�֫��}��ǙM�	��I���&QT��U�"'���r����X/`��n{Q�����Z�е�3mF��z���V�[I3~3L��C#y��B$T���'�r$B[G�1K70F�b�5>&I!�g�= �+'_
|����L?�9{Q�;a܃�,��U�j��(���1�J���x~Ҁ�\�q�w�{f<W���[gJ�x^P�F��7	���͔=\B�������O
¶\�>�������H8�E�X�=�.Ҵa���N��l�(��[A8�F�$0��,^�dC�iR솀KtS����q�O59�l�b.�e�#� ��CE�!�e���Ǜ�)�?���0���a�e�C�g�]�$�줬�@�_1[��l�RG����cV��`�d@ͮc�C����vd����
o���M?"rY~KtgćkjsDc�<���{��ˆ!��$�#�0�73_�N�B�ITn�p��z���~ ��;�/�}^9 3z��:��h[#D�[p�0_��4a��XD�����zI4��n}@������Ї`�N���Qwf�������l�4=OT���z�(F��7�58,���qX��#~�^�bU�n���hG���\ݐ}��Ov��R.�;������z�E=Z�%��b��Z�Z�a#Z����b���$�;H^��RTt�����܇q�Bw�7�R��T-4ǻm�����27��a�Z5�?�c�@����罻��DzBc$b�yY�����a #a���q^��K3����]���PEvJ��������?K��u��n�W��=5��W?�v����Y,ޭ�?���:��\iC���W��֥��Ak�f?R��gP�/�7&�I
g�14�������WZ��0?�n���@�ޟYV�O����aˣ ��y�'Y���4>
q�(TǞʹN4ᯕIVp6�v=�	�����:��H�G�Y����֙���p��S�&2+%;1m!�r,b��<�9,|��	G�[�8������c��e(M�k���D�N�%��[��2�e���8IP��ƀ�Y}6����%Wn���k���)����^�\�qz���u�=�\�,���:�<�{C��M+���E�a~`��gs_�J���i|��Y�v�]�i^���=⟒���z�|�T�����H$�U�ko��� �w�������Ͼ�5V���'b,py_P>3^�h�A�}���Ò�`;w������AM>�SD���d�2�����_�w��s}>�v%!XEt�6e���}�2+0U�p��΂Xn���7(2�n��h&�B���Oqi֌�q���eB~�9I��z�3��,Q6����N��*�^`�D�ۮm�{銑�-It���0 ��b� �Y'���="�q箇$!�b;�x=}'%��s��DОv䣤l�@@��Y��o�6Ȇ�����׳������D.�v~w.h`���5�l�3��\q�;�Og��i�g�M����+���@]����ƛ-Mm,��}iΟ$|˄u�Qxl��:oe�J2�hp"�s���hY��y���<W��F�9���u�¬��%�ֵx�L�޲���&���ܫш��{>#x�S��j¾:�z_���W���<|�(ak�[Z�$s(���]��@u_%&mͯ1�%��� �~V��+��;���[Ƒ�)_;��q���z ���3�:�ˡ��0�gF��rc0TT�O���j�T����H�LrdM|���h�rx�[�A�3�Y/i!�ݢ��7m&jw
�5Hև'����U���G��͕�2��b}�Q�	V$�T��P5�" +��!K��H�Ba���J7X��)I]q3�>4�2�W��
�MY���N�gv��o��*	����o�L�w�u�Co��r����U ܯ[�\`����� u����n��V�� g)^L$��_�4]p�o��Υ�<��ݼQ�������6���몇>o�wЀ1$ܒ� �񛓂����B������Mb\
y-�7�R�׷�@a5�Yz�~%��A5@�~?�e�Tw$��1>JJ�u0]p�`V5�:ʹ���NFE�.ع�G~�u�g8ޛ˥���������x枟����I�HO��DǠ����tx��<�\���6lN��P%=δ��'�� ;�CnN:C]�K�=��.�<�}���G����~s�3���ς�9���[��NĿBV�ԴZn+K;@�)��z�ph�!֤1�}"*�M�q4�1N�vG��Ǆ+�N+[%��h��䊃LN��Ұ�e�ž9M�Zj�CN��˵lƠA���l LRY�C����2�\JHv�p��`PRvG��}	Qm"��7�W�߃v
 <�V��UL�H�&�߱�
0$T���W���a�GƤA���ٝ��d�]t�U��KE;�LM�Em�A��+�l��k����_�Mlտ�����Q�ʹZo���p�5��C��c��h��ん��	�4���׎�']�8E�uYZ�m(��g�mѽ7?�
o�&V��%���A�^"��CR3�^��=����0[$Šӡ���,�T���$��KƥO��XlC�w��F�S�.l�$ ����D��+���Q�9�˚#]�v�S��l���x|�w]�<<�-!��]����@�7�s�A�������z��.�����[�uiyْ�2>��a�����7�>D6I|�64;Q�������|��:͒b�U��Lp�(~��q1;F�˖r���w�������r�~U]:�Q�A0���a!������,L���>#օ͌���Ў��1a��(���h*��r<��v��}��/��� ՜���'�<z�׬���U�Yt��~h1JM%�\^�虳��D��ߒ����_�=�s�(�[5��!lH뽯4��?����Z�W���!��n�wn��,�����I��*��������w�)g�����`1�U]�ә͕JH"��=Z]K�0��?�3��^\X2��k���p�%!�]�YI�GF�����J�|~Dvo>6g��}]�t��2��m���Y!]�/I4��߲�6��l�N_�-��^h�	b61�lph,���C1"/���^�xlTp×>����
���wO�S�qr���K���w�N�m#S%�ԂC�F.:op�2��p���+\�+��sC7�B_��r�6�7��l�iA ����Cw��C0ēgx\��H Jx�ڟ�
��&��0���N�"�n�:�=ݒfI�I�1q,N%D����׎��v?�_�s���r�h��Z�f�`�O�B���2>&(ew�c��ښ;D�Y>n����7f���1�T�L0�8�).�|p��0l��6��iJ �?T��0��M�OvO��<�ܷ��˙>���IĎz�q�e+�'R�I)��'�Ժ��U�/e����Lo�C��ճzTt��P�̾��C�R�8��܆���03�`4v��=�����ATS��p]�;>|&Wx�6���$0���2�H��x���8tSf=��@D{4����T2e�k�,W(�3�<δV�����6-�?�/��u?:r���붙P��R�T�3�����8�av�s�j��*���Z�p��V�>��Z9�z��k~x�gT�I�ܐ�}��8�d�c��͑~S��Q"!_L�f�!&�D��l��%���JO���BHN)�Kr��W�F����f�`I$���T�D�N��;#CY��������$�K�g_-;ϑ�I�����Q��U�H�/m��d-�bZh�ϗ��`_�:�y��G׎�T9�#�gC�0��_��k�|����8\���$����0�ed�CB���[�8e�P��������������?Z��t����o�Y�����۲~�ƞj�-�%�uQ>�j_��O�[�̥�b�[��} ��wj�;��Ͽ�h���G�_0��W����w���W����������A�^P���j_:����_V���O�T�N��&���C�[��5R~���\����ސg����\J!���>�.�e���D!����)��Y�+��6���(1=��[�sWj�FH&?|I7��
��֧���ܼ~S�uKzn	ْ��"�1���Di�A��Үo��:��.Y��F�w"#��0/���Y>g�[�ɘxj)�v�) ��0f���zC�9i;��ī��������ne�
�]�P�ߥTsع�'v������C��a�K�2�tB�E���.�AU�������fEr�G
�m	����;�pf(�J"F�l�u��7y44����2`,,O]Vb�
�G���b��gR|�����i{j�:�^�Gm�5�����L�]��+�&
1���%�7��A�V��U���I%�q���T]5����b�Ϗ�&��k�M�s���Z5D+��P���b4���e�o�q@D3��:���d�d����F���e�tG��h�.z���T�#�;1�4��/��taՄ��u�|�����[2�z�|��a���I[��jg�$#�W�M�F�1���jd[���?��X'2�n�Ө򣇧ϿޛM2M��8�E��i�N�^l;Xo�EU�����}�/�#��Q:�L��$7���Sl����� ��yH3^�:|�6��Ʀm9�2����q���!�G����Yy5Pk7�my���[WlQW��匝��1����\�����K�����^�.���w���0�]0y�_3��������gR�bs�$*�9���f鋞_�1Cű��~�v�J��|m������F��f�����ie��IZ�ob������6}/�u��Mˣ^d�לnj@���䆗k�dYŝasU)s�KN�E����o�4k��<�f����] 5���D"pk]����`�|�A����2V�.�g��&6��"�����}&0ъ�Zxo�t���.Qd�7t��<��T�P�dSw ՊM�q��S4�'[�"VǇ�d��Q؎��eA���e+���1Z��A�$��9���I��qJ��C���)�Oҽ��a��L��˅7r
?0]������~�����ނM�HAw�Kk��pBb4� �v/;�2F(i��x,hwN-��{:AJ�9m5��3O�C���{w=��T��T��Ar�����	e�E��K_�s`ܿ����jH*��5��Y��	}ț���~�����7ti���ZpRwR��?�c"���z��893|��y[��̇t�=�i> RMv�4��փ�Ÿ�a�V������$j���o���S��X#N�t��@��Kؚ���!�۲����Z���Z}��b��A��I�=o&��0��Cv�G������]	���]�[��M,����G�Əa.t~�N�������q���A�P� fl�O�=AZ$ֈ���c:֣���!�y��q��p�B��C&_������[P-f2�h��+>��I9<�<m���D�FR�R���\[>�;����0�u�ˌsU��13�����i�2A�w�+,)`'^R94(K\`��|�X�����4��c2!���	nez��}}�Yς���N�;(>VK��gx
�����ذ�C}�Ӛ���w�o�O�h�{tX�Pv,�Y_ў5!U71c�fu�kpO,')>7]EaA�k��g����II����`vw1����#Q~b�k����}c�A�*vi|w��4��/�L>n��k����~h��.m.ϖ��������}���3AĆ���S�SVp�br�_���tf3��fJ��͉	=MQ�Y�
q�c��j�Y6�8h>*�}j�Eﯩ��Lh&���y/�a���~��� Pl�=��̘�C�<��������cz�B�X����`�[����p	cWq|�z7���ػ�Bn�S���;-��G�!��f&e�;�e�ٯ�b���o�03xj+w���*a����]f�1�*dwr?^�)��ooY��JM౶�T�ᣚc_��ӌFx7Za���&\�V>�P�c �����t?�D|4�x8r�nRyhw�"�&v��n��L��]t��o�����:|��_�V�J�mm0ݝ�>>�r�se�gL���O$.˻Q#ܜdƋ��)cX���G=ɵ5�i���_4�uh���m>s��[��L�1ٜ
�}�h{�J�M��L�PK|p�Z�Ϥ��?�Ƿ��/<��]s����6����ú�M�r�G��o=��֩�j=�O�����B�j���wץ�\l�K1ɲ�?�!@r���}u��;�3�9P,�=�.R]���g�����SQ2�����`�~��o�1O�^$j`��S��cl0z�ş}��k�R�n��=�/]as0<	�.6bO�-�~�{:�\���������?N*����&��G�By����5b�������(»r/ge[4mAu��*'2;y��пk&ڼ��R��v�NR��W:9�;�j����J��ɝ�q�}���g��]��U�0^D�/����u  ���wG&�oz�����;��|��6	�uy>~�B��h<l�"c�e�:sg��B�.&�w��eϞ���/���m�}�K�����)yO�y\�]��"հ�i�����TzB��cz�F�����_�p���ӊ�m�u�?�O�*�GNr ������W��Kp ����a�!��-U�ŭGHH�6zM��hp˦��,?V���Xh�P� ��i��R�nT��k^(�ۚSsG���w�eO���hkqꑑ�XEig�~�h�k�Nڭ�2���%"]�����1ۖ�Nr�d��v V��pX����;l�����a`��Y����������2}���?����l���;Y�'䞴�[k��H/�(�����d��׬9vN�X}���]����H��*G=�J���Z��8�5���^,
Iד:bS��MGt��;�9(G� �����5����/�u�렞;����CsU���rٖ�e~o�����z�_��f��a�7� �`�|7�o������X��==b�L��>�1ry�ԃ���/fI����0�kL��T/�?��2,�m�w'�Kpw����	���N�����Np���nEQ/Yk�}�>�{��_�����7gU���[k}B�[�~�n/ԏ�ZU�|.��vq���
f��k��o�Ӭ�uA��Hįٰ�ˏՍ��W`�9ԉ*�w�"F��Fnq�UJ新�㿶�<Msh�ss���~ܽ(�����y�\�� �
Z�kt�A�����F�K�������j����r�x`�$�'��E�o5���~`Zrr�rX���o-B;.��ɳGwU 䓦������r��֓�8�j(��L��!�?z����y�I�:�4u3�Q��w�"�>�M�bG(��ٲ��%���e�Iل\�\���-�P�p��{�U����B��Z
ulNe�!Svb���{�Z�?�oo��N�1��Fh��#)�LV/ ��-S�V��q����MG'�OjxY�-+��:n當����49]��ާ��!x^a��(�+z�A^�N�vg��Om.�Y�`���{�N�w9՟�������ˠm6QYƖ��E�	܍��)�xqTc�+8���]ݺ�&H�6������]�E�M��[)<�Jgu�R`F�ё�
��7D�$�2��ond������_��t%�%Vu�9����Q�&�죲�����{�:�돓�i�̴ʄ�4Jj�
t�ulE�8cG�o۶�J����"�g��bL�2��|��@>�-9�^rǞ�\�4�;V�%CSG&�W7����~�ֱ��(��$a����ц'��緔�{2OY�˼@�A��1/�˵��z��z�Z�B����H�M��9Z%W���Mw�>ts�~�����_C��K�M4;qq��\Z8��n�J->��x�j����m��I�/�B�A��R��ȭt uC�e��v3�_�r���:����a��AE�������ꨇ���ȼ�H�>r�ٿ�rM���*��4����çiꝆ\^���e���x΄R�O�|aY���|-i���l{� �l�4��B�z~���3!�4��A�'��|F�&�
�Ô���m��ֈ�{hM�ġ��R�N7�KC�_cK����ƞQgs�^i�{�E�⼉kq�fg���`�R���i��g��M(�.����,B���R��v~�hQm�M+���x^���m��_��2�#���k>�~[�̏^�\�Z[����L�ml`B��d�r������7xb����3�q���.[Y�"@x���z]]�:1m��������T/�tD%�!��|�$�JT�M�=���j������ѷ��AS����=_iDK?�qGz~�9Hm;ó�݇���i^Y�|�C��}�_;��H���P䅖!N��]v� jR�5�f�r"��}�a��G�SM���ss��fТ��vG�粻�x�mq���p�#�|@�)���M
xk�����'Nk�#$6�sa��5C���u�Mr��w�+�,�+	���Ⱦi�;K�f�@�D^�|{4��5~eE^R3����^��M����ӝQ%sIfҘWk�G���z].��"@W�ƻ�h�� ��/��F�>�^���WN�Vt�q�rкh{��}���t���m�Yq�D�bC�Μ@x�'C0v�O����CQ�Qg;"��ەf����u�^�9���	�^���eȼ����Pf�C�j�T4DO|�X��Mr�j��I�߮�t^��ܩ�����I_h�>�(��w�����>��6�/����'�d�G����y�L�����VO�J8�@K���~�xx��j��k��Ln4��-��6�J��j�s�,fi>�ZCu��?��=W�~�]����wcEv��~=֦�%�!�*L���Ru�
���=��.9�"��|Y�'KT��_P~}2W��dN�ήkZ�����r�;&Ab��W�vi�g_������y��fhzr
&X�S�Ŭ{>bds@!���t)3�/?�W�8�3-/��H�L���&j��Ѧa�8�i/��4W��
��Q&��*s(��Hg�*�7*�a���#�K}]v�ο�ȯ�!�:U�\ρ8��.���ܣ�bZ|�c5[7��>o�'j0��m�w�`w���"������T+-�,J:�>J�Q���XWp	_��S�b�?yj�)�"��x�M&�B	�%Iy9#b��(����}E��<���ZlO_ �Z� M��
o��j?⚲Y����whcK���W�^�����ͤ#�4D�d�P �-4r~�?7�^I��Ң�JoR[	E���/�����ҏ�A�f��N�oM
�k�E�
*���s�{'�U6���)6�.'�-��l��֗�H�G����-�Y�ӣzJ����y�7,�26$���ݪ������{�Ƴ�֍��f���cfo�QL�D�QcW,�v���yp�|_`��5���uH��u���ii�-v(ľ�(�i�-�J�7u�-�E�^�0h����Z���P%kk�4}���x�%a_P7����):<���8
�4� M�pp�ļ�}��L�մ��Vj�YF6	e�����M��Z���ە����c)��x��d<�7�v>VO<|t����wo~�f��m�:���*]��?�;qg���ơ[Ƥ'�:�PZ:h��l.&��5p.E��o��Lp= ��p�����<�ԟX�$y�&�RF'��Ll�^� \�b���.+��oK���70ɋo�L�T�տ\{��`�E���s��F&���g�@T}�A�2�S,K�
U|մ:���@�2A�Jy��Vf�nh�:I�K�Z*��kU:��[VUM��H�dr,�H�NǜMҙ�~	���Ė�'b�0GY�V0���F��t�*�ϖ�}å�w��@^�s��:�ٻ�=�ٰ�?��_��_?�"סؤ�B2Q�|�1������{�6*����G&�[�/ M�\��f�G%��+�Q�k֎!�3؎���y���fh�$��7�6�~V*QHxD��ّok��nƃ��G���7;�w"ɤ;�|�NMC}��� ��J�% ^�)��6;��G����M���g��:��oڠ���EPk��M4�퓡/��C��nR���M�,����ױf�}�Z^�p�hFï�$x����Lx�S�{>�Ih��QsE�Q���%�q���-I�f�������w���-�p��!�b�_�*�^8��,ɫ�̅���`�mg[:�uǉ�j�" v��Ut�O蔣ghttp�?��Z���J�*Loʥu$�O���t{)\���7��1���ʗ�#��V��m��n�[��M�u����%��v�:	����/>H$��m�K�5��A"gbZ�qbҰ|K�V�P9W��r��ҫvC�-�E�/�;�C���<(ϗ���g��X�8�oY��}�`8D*�w6�¨���XL�޶ zA�J����u* ��{��ir�~���U��g�ݲ�ڡ3�	pH������xQ9��ck���`��>ÑgOr��!��F>��Y��bT���o���.�<�āJ�9pё���\(:�"�
0���3�4���9
�V1���G�A8g��k���-�_5����gvQ{�9P�6�,���q���A��o�<S@�&+� �����n�֡0����ߍ�u��J����*r�,�ڏYc/ǎ����f�
�#�Ȭʹv�E!6����sA�����ׯ膢�Z�l7J[|��j'�dt�3��C�r��2�cV��}x����E�[΍��X��aA�q	�X�s��B]��������|��.���6��~�b=s#u���u�{�˵�pZ�A�Y���x�%j�z9�?�
o��ۄ�"yRՑ6Uk��q�c�C�ء"p ]�.a�^�n��)h���W	):�j���7I�� T�QHK�?�1����\<l����������8��٨B�΢��oBNk+�>)��*�ڞ�B%f�Dd6��DҺZ�j� Fv��҅�7���5a�`�F�S�K0�0�,�o�L���0H"�CNl�9�D%�~>�]}-i3C��ԣX�P@�y��#����#%��+�\���`�c?jz���e5(.A��$�B��=�x�;^ʖM�Է����Nx����E�
�W{p���o�(j�n�k/D����H���t+�ތޚW��|W���ל��S�U��;�Z��k`��`�.����!��*qsH��@ꏜ����B��p��������E?Ga�����\*u�����oB���#�R�4����>
	���5�5�k�/�/�O���������^vصQ}��3��j�Vs]�=��2!*�a1�ļ��x��>�1p;�q�"�Aղe��4�u=�~��bV�5�GCzaL�9�5[��E�;!�d�w�}<����G���6m�^�tz��
u��_�+x�R�CW�@��;��`�ݝ$u>�^G/҆�|r0�ஓ���L����Y�a~͈�$~"'嶾m��Qn��V�Qs�)�X�XEG98ոb_��4d�]���)�}�o�-1K:H>H�g[T���_M�c���Um?��Sl��6�(��E��e��v΀̻Y2�&�=�z�d�ȆZxʮ�	�l�*�����Kv�f��V)��C�8� �p�=n���d��G��5���T��7F�G9�	�˗�x����/�s!��O�w�>+<uΈ1Q<]k�������ǅ�7/�̮�xM������)���w<5�ٿ	�G��"�P'�;W�ǜ^��N'k�c�gAD��O�U�^s�T�O��}W��%�A��o|��$=���O�I��ݮ��Ƥ����~Exr��|�m��D��Ꞃ�b�	��L���/̬���/�si}�(�o2�[�u����e���.ߩ�K���نg�:j2Ϳ��YV^@\��Y3D��������;5��ߩA��������?qɡ��gƑ�r��L��#�^$�7���	�ϕ;�?�{� d�����5������g�5# �n��$���~�m��]?mA��{L����h�����A+O3E��]DKSޡ��f�s�� �2���:,VG�[��IS�ʮ9��R	 �4;Ǥ��J�����"����A�<��
T�þ����8��G���������:uV���ov��TR����9�X����ka���Z�^	�,s�~���Z ������r^�1|u�,���x������;�{�����������@PEMӯa�^�G/�)]N,���~a�g���F�J�s�5<5l+���O�&}ؙ�=�J/*_���4]�.ʻ�?Ӌ�x��G��V��F����]�u4�10�g��BrO��[�|���p�{�Fcj��O���>���۩��- J-ۣ�j�_�._�{�/�ኟ7W~�c� 3��Ϙ��p3����h��ž]�Mԏ����&��K���}�}X�A��F��Q�>Jn��B�XL"�u�oė4�w%A���!�H���<b��`�]��X��V���Z�f�#~tۂ�͛���f��>K��>�Ӥ^�`����u	=�'	er��/$�0q* �3@4��ҍP�u\;��9(ժ���� uw�1���Q�`E��^l!]�����[�/�������*��*���Ʊ���>�>Iǽ�P�q�Yc����T ��Pށi/O���	���0h����#����T�5�O��$�ڀ@�>Hѣ3������&��zZa���%�&b��W�w(��Z�O���)Z`�H���H�*2�]�����6,�ҟ�5V:XC�Ż	��!Rc��l�)��x�R��Pa�jq�Y�0<��H��EC������9�����͆d��ٽ��؛������2õ��D����1�	��|g��b2 �� �S��&D��L"�����9���ҡ��Q3����D�U�p�͢�22����@�4P����w�.��V��	;?Mώ��<x�[䞾���_@̎�]��r�Y���+���䧷O�ӝC�w��f@&t
�{7�W��ز����2Q�o�x|t�#��>@�| �k��Vo��_�xs�n8���b� R-�w���iϏ|�X�c`�	M�ȴ��Oe6��V���&}���@̩��!Qw^�̴��J�=�"+��!]�;�v����Ʃ7Vĥ���Jm������wTxA���wNr�0]�W�;�����U q�m��}���X%I+P�ՙlQL�����qˏuo�E��������ʉ�56�&�\nR�d��6\�p��i#��_���o4C����I����`�:F�jPIȇ�����80���	�TTQE������C\�t�/�BXl�Eֳዜ��(>W��D�9%%��V�M��.��h�_�z�C1}��^�y���ؼb/J
�q�:^�~lS{>�*�P4�F7s.Q��g��Sk���3�+�W�q��܋`�>n����|i-���E�ˉ����+4���a�Ѹrj
j�%t7E�w�±�a��	ɔYkh �U��<��Ȉk;�����4�]�Y���u؄�i��� ��cr*s��}=Y
�	�v�-9��:��p��e��|�X{��#b�r�>�ʆ}�_���8���x�Z��cq�09s��@����a���l��1�u=�w��|9�*ԝU��z��mJ�����QTŇ��
���1�c���oʧ㝊RHB���GT2*�Bh3�t|R���nf���Ȉ�0�fU#��w��wº�z��5q\�O>2�|F�{nAa���qTc*� 6q�����z�ɉKÝ헯o��ah�y�$GGïN�R�c#��R��F4I\����+�f(:�������rp���7Gq��(�B�h3��-K�OH���F�=����a�7���������T<�t8� d�az�yBdCKb6D~��X\E�D�,^��ވT�'"TqX��7�H��i��7=�!y�+u�z,�	5�Ͱ�ѳ�;Cu�LM���ù�ˮ"SO���[.��y��=eVs&ǧ��୰������_�.���� �o�"Vo��v�O��ɏH׏Px��h]
`Z±�L7GI��"s ����D���~6I%ނ���E��H2[8�[�'��}�LF��h�[lT��a-�A:�S ���%m�)�V|�A������G��.��"iV?r#��7$+X�$���5&>��2�?Ł���8���0�!�����I�:��h��do�����6����@�b��~r�Ř̖�<����[�B��b3شg�ɼ�֤6�s;Z3-oH�C�6	*�Ȕ��#]-��K⩮�H�d��t 8��WTG/*����OW���R��X�R;.!����9��n� �,��XJ'\������o����O�5�A�sL^ ��7��;e������W��U�Z!>�j�3W�� I1����p
��1��W$��>m�!����}�)��pCKO�a �1�t��[M"���ܤW�	ԦB�5�=���c���G�ȈU�E��n�q���\%�|��=�P��c� ���*��U:����_�	V~�֌�B&3N嚄,b�+6�i��T#���t�bjt�t8mf�R(]�h�������9YG4�k7#�0�V���e8~7G1e���<fe��,��.�>a>V5��s�@�Q�U����H�!X�D�__si�wwn�;p��)�������w����l-5|�Fcf1gWX�L&��v2�1!��ja��7<��Om��}�%�CI������Ԛn��< c��0� ���Ż����Z��Hn=)��#��N{��=��NB�^������$�u�-���{ ;�.Q=z�)<K��ӓ��4;����9�戄̰�n�+�vyrC*!}Q�����k�I����	�S���qC�j7jʺ�Ϋ�����4���K��Ho�Ap��9�_��Z����}�[^)D�Y/26ъ��]����S�����7E�lE녽��Z��o����~JP|}��%fsi�:w}�,�ƌ#l�M^�������R>�R��/�M]���Ҧ�`$f��0Ҕ_��s��#M��-l���l@������_�Дh�m�z �v�m]�;O �t!QY,��~��=�K������Q�ϦГ)��u�*!����ax*�
�7�m����?ŋ.�(_��g.��u����G*G�W�ݢ��Fp/�YVj�p�Wj�̵�V�*�� �c���)����A��A�a̙b1�7�X��%�, ??�b��ۢ/�˙^���/D�
O{l�!z[!$9mglI���� enū��OY�/{%h�倭���O�U&��o���j��v����o��[�O���d_nP��4�Q�w.��(g!�����X�UU�&����]��y�!��&��,<��&����T�0��qvd�@�?����yx��{FWБ9K�m�:#�6	���\S�+o���q���Y��Q�R`I��.����؉�O_�01F��5ۼ�%d��4���J���������:U!���Bz�����N!Ꞹ-��/W��@eA~{�������{q��fR�z�x)�9��<{<=P4{�{���;���.��j�ʵ�T:"�:3�56�g�
���(jXJJ��2]n4z!�9eY�s��Ț00م��C�>{wO;'�~�Qu�~�Kc'f��]���Ꝣ����/-�p��m��OYm��iߪ��%o�RM�������1%�ji�� �=B�i�4�#wP(��+����ړ�z��*�mK��w���*��s��c�o�¦Kk���3#,Ϋs�"f�	Omy�\�v�5m�!�	�t�� R��,�*=����%��Ge\(rކ�	�R��%���3<"r���7^}�x5��ǯܛ���4���L�$�%�;��E#�&�^%&�_�>�G��c`�!#x�%rR����>���A�>d�*��W7ԟ� ^!rku�Vm�>pыn�ܭ�ӆ��Vz�)���_M�!�Y��h�v&b�w��;%�	��9�yj�}�K:!T��@�ĳ���Vǯ;W^���t�c\����%Ot�ȯ�UΞ�%���(G�O*���W]k��g��^����Δ[�g��m��� R7eȱ1����p\	.�|uB����i@�He&��K��F�mz��t7k��G�XM�B03�OڡJ�Z>�1B�"��[�5ŭ7���S�@�U�
�HG\�g΀[����	��#���֍:���镢��
%UW�Q~��Z��C��̺��s�Rl�g6^��#�SObb p,�1���8;Sp&�*�t��-O�(>Ο��Q��JOk�n<�Q��#��\r5>t�+/6��@
���%9�������dx�4�Φ���`"jO�����Ȇ�@���F@��<��g�F�#i�B��za,=J��,ɗ[9��L���D���QX�?��	w���w��Jy\�$n��?3#iWj��â�"܀�ӷ-'r� ��Uv��%1}��l�Z�F$+�$b�~��hZ-�; �و[�t5�FTO�o���(,�x���Ё��lʭj��r
l��������w6�����=�?w斄�9���"Vf�G'f#�_t/!1F_9D���0�V�<����%���KF�'����ɧg���O������GZ�Q8�@A�nBi#��_�t\}wF�����������J�M��>B�o*�*)�C�ʔ.`g�\�MX�� ؀
	���9�@���?����o��i��h+�<_����c��X��EV
�ε���]�-�>z�V4¾����n��l�y+~-��x}lP\�E؏�m[{���f5?z�G`�۝��3;�.��+U-��p���㚒����_��%zQ��O6�]��l-^k���+�zq{�ٗ_9����E�o�B%�4
����>׏b�wQC#��}���1��)OY}K�Q�dZ&�P�c�b#�'^\�~�>
[�r �Fp��(j��KT��x�x�z��t�2'��<�6�S�ve2�]َ�`������b�_��@�|�L��%~���E���5��?�[J"�b7���aWM"$���uu�oFX?=I݈s�F�{��v��Ê��}j�9���z��ec_�|cD��Fl k���HQ)��	J	��`�7n�2�SῺ~�?�Y0�U{��atl&�<�e14��� ѷ/<�}��'��x,rzD�3[����N�l��Yz(�R�=b��,�E�o���^�m����@������O7�qabE#��)��w�ҔB^�3��2���}g�Ɇ�^�+Zl�g���(%|��	p5��҉#�4F?z�a�4=���R������"�9%�%X����4�B�<΍�-���x�ix,�,�dI=<��`������}�h|,���n�ȸL�:s0ߺ������~B�A,�7���[7!<�kX\�oTh?:�ѭ_��Fz�U��{^UZ�FU��{x$��W$&z�K���H����h�	�n��j�\��_?JV�n�38e��U
<M��X�2:��qq��*b��|�������n�msGc��线�kf�U7���S�g����楽k'�O��ëez5u��@d����\NՒ�w*ԭ=��\�u�q���`��~}l<u�5����+�Ɋ�+]�(�9Usj�����3�(���6J�{*��[fq��Pǵ��=[��.3�tBRW�2��X����c�\̱��Z�����z[����Դb�xO��@��ky���Yذsk3L��㴬bu�5}�cf!<�8)�2Ma.k�y��Кo�3�?�������J<�7��YU[/��ޗX���פ�e��7?��K���x�%Hs�	�7�ua2�$�uB�6Q{{1�`"��`#�ֳ�i�c�$���$�<��yۆ#y��ڊXͬOuF�����k��h����吝.u�zӾ�+���m~������U�=�+��?-���
]���T�7QR�騌L�A�(g�����}�G����g�,^vT�m���L�}�dq��{>�s�d�]!a���#�5��`�!��h�:#��/"�����39��m#Ɍ���m���y<+�_��z��ރ�ȍ��ii$����I�=΅�x~tVТKiK3IȺz�#8S��1Q/�V��ve���9�f����{}:��,^����x�G�*���\�.e7�}rvf8d�;lў������2��/)�9��H忶g�����u�����lY�ˆs�'�;oV��`s����.7��s�5;.UH?������1���7w�cb�Oɋ�}��XK�?�����/E@��VCz�c����a�V~k�[
�?c��޻�I۾Pei;q����7@s
�6��F���Q��Wt�Ԧ �\b]��%�.��������v�bo����cy�n�̯f6!/�O�Nȟmq�~�[�i��B�t��H���t!�G�63a(�B��$�͋�n��̼���'ۙC/��7�[D��g����������:�J_��p��#� �n�/ �?�y���5*��y�x{���M�j�aL�p���ɄL�h<��W���D�7"�{n}�ƭ�s~�Y����Kg�w���G`4s;��f�:�)7�~��vS�;����^�����zO-(�.,�	���f=�(��U|!$�����g)���r�Yu�J�>i%9}cY���a�_"N��Ў��{F�9 �AVK�9p��ə�Nd�N|U}��K�H��U��7
u���?hƊ�km�px���q��
ڑ\����^�����^��r�i�{��5K9L�ǃ�J�Tϗ�k��&���Ƿc���,�(s�Lh��g���N��k6��-0E�n���zF!������a��u:Iv�,`�IwO�� *��;��
����n%��.�?R\G���8d�=~�Ѝ"���T��z�^	�O��)c���bl�J�t-� 0�7���4�gx0��9��ǳ���7��G�����*F)d=u���S[�a`����C���X�;���O��1*hh|�k�SozL��0ΙP�m9��r
Vb֝~ur�Z�43Cܹ3��yԜ����CrJπ��p��f]��]J�����Ѧ-���@xon{�V�TH���r!�q�XR�,�ol�:I���v�����y_��\���?�6�Q����yQx6���C�o�C� �~�D�"��Ջr9 Oa!���Ώ����n�/��]�i\e��!`��1��-ͦ�%���|ϧ��:�q�qCzi��$��Qb΄��n�Yps����I�,SH]xD�^��>���O���?�v*�p:yz�+z<Qx� Ѿ�=Q�-T �)g�o 2#�Ӯ�G�^��;P�^�9,�5�����#S��*��y�ς����T:���y�M.���y�0Ե(�[߈ln�����p}[��5Hb202o�Y۔t��}�p������*� �F���?Ae��bJƪr�����PS������9�&f%���}�!�`x8%���[Q �R��̇E%��D�3�JdnC��\	p���˘`_L^Uj 3v(5B>2����2L����I�u)��'}o�汆5���N&��#�ٚ���ڴ��"��%��{ Y�����сu+
BcYk/�5�芹�.�;�NDn
��G�!� "����9U	)�0�q�����¸I��7f���m|�#���7L�@�KE�[��o~>�Ʃ�':�o6��	��Z��\X'��V��'~U��ի"�����I@/,z��������w�����Zs���4C&f����R�/dx�}[I�m;{K�l�����+���g���I�.�k�GƯL��n�#�س���7���	0^����S&��W���d�HN��t_������B.,��r=�<��v�t��$�/�Q���C��]}B�����L���YJO��R�S��̶s���M�mL��x�3��*zs���&�dӋ�+~��x5�%6%�������C���l��AM�����Z��2;cdOI�?��6��@X����Ҍk�x5��aA;�ܨ���`�3�	Hb"X{���2��{A�.��^�;7'17�^7<�K�Xy)
T�m�`R�=�g����q�ܧ��e������VC[�*�n�Ԝ�:�z��#��E`��d-�2�n�̷�t z�ǋ�f�ɶî�n��"�������?���r"?<����"��Y���@�����A7�ꁔ�")�A��,7���`$W8����� _�K=4�|���K����P�W� +�폞����^x�B�e��������Š��)6_�AȣƵ'#���Z��/�#Cj���_C_S�# �,���LfB��h��s�<���q�_&a�:"��w
��C�<��V���B���	��HC��Km��Z+\�X���؅���� Q�	%56�e�5@�b�6��9�6���2�9�K�������`��e+����X$*>\`T�i�C<�3QF|��d6m�����]?uBe@?���|�7�jQ�vwSq>H������f_r���}�7�r��@����|J�
�K��*�J��1(F!T-�Ƿ���Z0B���R�&�!��10�8sF�=��©;����GZI������vn�0�̮ޞԻ����8!��vt��@p�-���9�I���Ġ�`�U�}�i=��k�f�5�bZGܠJw$Tf�����B����"����d��YXT�a5�������{��\�y�ߦ��0V�:�2B�]n������5������Y��M}͓�șc}bJ�X���u\��_��1N��3[��G8���+��hI8کt�#��1���� �[?0ힲ.a�t(��rw�u� >���㳱W��)����l�+���4�����L�/g�^iSwt�i��o �J>x��a��p��I��T~���Û0FN��6�Ed��|l;���nv�����m��V蚽�;V	�q4�=]����}��]�`u��k^��ք��wYq,�ԍ��d5Z�`H߅��R��82+J�Py���ǺG�U�~��C�t�]A�tsM�1la�}�Ǒ�q������a���II<\W�,���v���=�v߰��w�=!Ĭ�dE�D��	���)���b�f5�g�����j>8�$��	ɛ�_-B����@��j�+�^�<ʌ��g��"�W�H�Oܠ�5km5o�_&��(� �z�!�k �`���h���J7R�X�����ྣ�2f��B\�l,u0��g��j�ohD���ע"n�_�y�w��f3�3��;��t��I������ Ҫ��ґu�@o�?<���a/;��"��슦B���l(�# ʷ��w��I���h�	���Ϻ�ng�XIrQ1���׻/n�ʿ��I�؄&�b�vh?��%��s3Y�����}����MeD���=%%���{�����������ժ���ў�����慜�A���"|IW�S����	�m4���V���T���eJJU��x�F>�����7CT���t]����On��֣��T���R�A0��(WY�%�ٽ?_t^�Oef�[r�蛽�e5��4�Q��q`�olI�@�jZ/����@Ȩ�Y4B�l,΂�Z��[9�%�c<�96�)��=P�b��XtN��4C}��S�Itdnh�/�P�%���Ň���^3��$��a�x�~:b&�������,m���_���vh'j�^-�ӄ�4�OB�vc�ÌC�[�Β�﨎�0�����&Von�8ꭗ�Ϥ�r����5���Uj'�m�`�Ǉ����
�)��o$M������ y�z���I��> G�����sPٷ8�4ܯ�0>��"�ˮ_1(�m������t�)�2�k-d�psC��C^�nQ�>l4�}a�sS�܈`b� �.�>w�O�R�n*�R\�N���x}BY��������D��,v�z���뎗��*��UMǬ3��"���H�C0j�m�P��3F��c���h�\&�C��q=%~f1��O�S;���j_���1{!�2D؇�[��t�!�@�-�}*���_u�`�BE�q�e��eG��[�V�NU+�VF�@������A�U�&�_R���ݦ��k�&`eaFt�ߎ�;�ԁW]�8X7�V@�H��&[��?�n�����$��v�^!`�Y�ed>/-F4%j��6#d����{k��_��<�{M�	K�o������������O��~��;jՐ���:����kT���=��B@�C|(N|ɛFvd�Y�L�n-Y�3�����O��'	���yW���8�Q�~v�{�C�]r���T�Z�+aM�	]�������?�<:fg�Z�0�$��9�<o="b�"�Г���CB����L�>�� j9I>��6���Hc?�/i|��i��\���m$7�tkᑁ�eI˳}��H5An(���_�c+��������%��>��LZ{
K�J��l�c)�_�I�@�cw�N��I�����`O]����?��?��#����9W���f�;K�żc{��E�~�:@�Z`�m�78ҹ�gMڎ��:��ӷJ��Rb�W�����	0���������w.\5�c�wB-�?�xcX,pJi^��L?q�H]� ��.�ó���Ei�]aB�o�:���j����ߑg~�]q��KA����+�Bc�sV�5�ۥ>5����<�蒄���?�*��%���������4����q��4�N��i��cʗ,^&������)mV�$56�;��uʽ��WTAd��:倷5�kEx�����5���K[m_d��E�KbS1�?V666n��74������?��C *�Y��6ˀ-�Fb����/<
5
׳���Ye;4/���fS_�H�~uF�J)���)}>(��`G#��sr#���5�f�CJ�ė;�	���2̒;�t;a�ɔ�;��x����C��f`y�r�~nS�������3�Vx\jŧޅ�j��bHk�^A�Fx��m��!c�?�b�$�r/.���~֥�IZ��6�n����U��\̺������&�C�S�BՄ�++r�7�k��h[�k��i�8y!�~3(�Y�lt�Ɓr>rQ�%&�ҷ���0��=��N犒��60�t��A��|!���LRU<s^����Ǫ���G^�ɰJ���n�S��@jS�au�1hbE� BVO��[f�ɬtDVJ��^D@=�9y�������aH��q.F���������7�~��x�]4�%~�p��R]���8���4c�h��.v�>Δ�nxV�=�d�y�,2���_w�7���e$u���a��3���E_\�ʑ��٩�F���:�*�
���u��3�(���������C{�*+�R\��ŗD�=}ɖ{z7��%����h�'E;w;#�4�~[�yx�)�_��r,�������$�[�:���s6�T*�ݡ�
�)k�}�|�=���8�/2\���K/J�cuzۭ��RO���*����R�~�����Y��w�h�WMn�O{o�֮�&������]�K��A���������޸CpwwB��'$Yk������ﭺ�v�:�Ϯ9�F���x����*�Kz�������7�e�u(˅�ˉ�<��A�pI�Ru�$}����_���h�c�b�����z��t|Į��E�UKK��K����u��Q7K�G��	>\ۗ�X��K(�!��h�X��(�#�[L�|��D$���������E�F�!�!i9��mr�Q��~C��襵��66/|�#E��}�[x2��5Ϣ���z�a6ڴ��� �CX���'+�Q�TȮ����9���:5�E�t]~p���X��������7Yq�a�.^��6Q�&���huh)��ǹ� �����D>Hȱ��/���3<�4N��¿�=ң�?��T���}ќa8(4���zc>Y9��ꀗ�S��#V��MC��+�)��&��1@�|�&�a�������E�ea��~+E�5ff�1?9I7r)k�].*Q�s�W�|]�Ml}٩�p��	�v�$jV�H��M�>!}��Q��_���&�_�^m���e�Oؖe+Y���v$��O)D{Oe~�Z�đDM���Λ7;�J��[/�a5��j�z%wd�Y4��t����9���3�"\��VYK����:�*è�>"*���Gt�ò�u6�䰹@���Pt���>cB�g=aN`����c�<�3� ��=�e��C�հ�.	�s Qxd��TY[#3+>�b���"�;R����@�|+��&���1;^����� �4�lxO��I�����obb%��f�i��a5:!|ܘE��YN�o::�k���ף%w֕�O�ۍ�`�+��7�(����<��2U��
>Qɹez��_V�Pj���S ��0���Gn&���{�e�ڼ�Z6��pO ��w/����үFE2�
}�yU��*���4
��O�"7-�6�T�`�XR���[RZ��nk��Q���W$�~V�� ���.��w����_��lF;��.��ކa,��;=O�����k��wLQ���͑�|���B��f|�u)�p���Y�.�q�8����$ �<MXe�W;�+%r�)��2��|u�/�����i�#z	ͫ30��Y����U�e�϶u���6����A��uy�,�æ��P=��?d�w^��:������M�ݼ��|ɼu0��>��V�V�t8���S�������O�56Fݐ\;(t�^x-~�s�3E>y�K��������nHa���9�oE���^j-��sC=�F�r̯�(U�
�j�r�!���>?����wA�j_�U���@��z�V���Gfа�[^;����EL:���FZ!,#��&Ө��D�Ӥ�qdW{��l���m�2�(u����D�{���TI=V��4N���T��3�V؀C��z�{jC�^B|��rK~m2ek	->Zu�}�MK<�wN����e^��W	���! s��������9�f�߬,a��*T�'] <�tov�C�v{��,YK����-Ij��t]�%!A��*H�#Ö�E�nE�����3-��`�?>���Ȝ4�s�U>yD���I�|?�?@�[�~��l�d".�]x�"Jm����TZ0(��U��?��+����x�f�EscLIV���{��I�qN���˟�ԏ���OhЗ>���!�I�����]Λ�9<@nv2ڲ?�=�y��'O�j�ׅT_���v�%Hv+��/̋Ԃ�NI�����#�֋d�Qk����^G��n�����։���ۧ�*�\_�g��E����]��#� ��;��=%�p��K��3g��c{E1A\˾�;̕z�T�������բ{�_orS���/ A��7^�y�� �DO�����A왱�嬁��F)�Jj��K�J�UΓ����B]����D��EG�|���[^P�Η
wU�R�u�j����ۉj�kf~)�6���?�N�a�9>I�<z��;�č�t���r�/JވN��Mf�qaD>ʥ1�� V�5���Dއ���I/k[P����~s�q���$�_���bA�e�,��o+m~��:DJ���.^��?�c8�����Bg��a��W�`V�=2A�W/0m�yr��Pgd���\�hG`��F�t�I���Ո?!~XbM4��S�\x�F�vz��/o�M�AW������Fn��*� ����G}�7n��c��ӯ ����ӂ��i\����Ό���=g�R����`�[��V�ɤ��EE�{��c��S������_f|�x�VHm����,똄}�s_�]$���H����43��ӂ��v��te��{7a�z��p��"�t�#�l28e�O�4���� �u�KEr��*Pr���O�Ъٜ
i�!��R}�1�.^
71�Y5G��̍ri�����Y�8pC~����pc{�U<�fcbΨ��~%���O���p�Rp $�j�=���-]�ܠ8���6�w  ���7W�e���	8޻�La�^��<�l'Xlsv���+3����9�Y:]���+�Ts�ڶ��Pa:�p�hJ�Uc���8��g�R����wz�b�N�GY�Я��>���Ub̓>����3:Nφ�x���.�3Ӥ���v^�����3�?g5C��8�U���#D������˝	7�e���B�|N�5���g1I��T����3���.�R��[��zS��A4��i��9��8��^��DK't=g;^�oe�Y�H��Zl0	>ŔW��2S.�C��aj�(�IQ�0_J���RG0�<�)��J\[�L��t�k��}�[��}�P��I���3�g�ds����֛�'nvg�Il�л�����5$�ʺ���6�9�����M��f��#��+���pປ��|��p���zz���_��5�x���2q?�����������r�6�,��XBIp���p�Tx�9���5�\����0��N5Z(����ˌ� ,	rj7{
��
 �t��c��G���I7���]��myq���2�����U�
�+F��.���<�G���Z并a�Vn\�͚a�K?�S���L�@����^�L	����*�|�3�AR|�ƪ��\���⾝�{Y�P-��u������/�43�	NR���?�E�9�kaٹ3��
Ɉu�G|dҌ����E.,NЄ��{�9�dz#9m�j���R���Cw>�S�>�
���C�3 �N
@��Pؙ��(*��Jm�S?��(��������\tZE���&vm3߫���e������������t�|I�7YY�w�x�����&-����=�3b
���ҥ��̻ ��Sh�l�_����G?�(z�糢�Q�81�*�)���"9�[0t�׸�Bռ��#|_��ps����:��W��je���Up��"
/�,n� �;��b��ϔ�3t����dA��6�����{�w6�8eG�+��a>g69h�u(y-bo��2�$2�L���%X�(1��C�"���bN�RFR��gC�����R��a���_)4�.ʎ��L��!qM�0��_T*p����r=W]���rr#b�u/�	r/D�ځ ;<U�F�+nV��-�2����_Z!�@�V�%���VOY��η��fAf9�<��������K��V���D���!��-�;��.Eݥ��Ls�R�2��D��|��aM�M`ӑ�Z	h�����:���Z��?��>Yg���?E#H��3b:=|P\����RQ��餣����B(KӪ`h���?�b˺vg�����	.eY{�&�Ø��=��E��Ų�n��}Up��eDqg�@�?���0�c���^'�q�i�������v��Z<{�,�ܺ�N4���J�.M�u@G3.l���㍳q=��a�@S@m���|@T�^�|c����3fpt��[7�i���)�8h�	11��R��i?�1ק��= ����rpAY�O��I���JBE�(}�\{�u]�h�M��5��gj,�>�ʱ�p�*z�P�����/��4%OjĄ��/>[�Bhl�����J��DFY&�i�j��.W��'��S�����y�;������3�-檅��T�CQ!�t�o�@����*m��J�/��X� ���޽y'+܅��&��8�qD^YP�{=]Z6�iTڣ�fR�X�+@�:v��>ȝ����RA�J�����!dء F`k��Hg/��F������냶zJ�����Z�|
�*��g�k�;��������"4ҁ�r,#8�,L�i��#��ו,iB���}��Į�}��J?�YulG�oc���*�e=<c��6kI��r3��"����i���"ς��g<�h4\�[�,{&
�yҝ.��:1�jfp�Z��Z�1����,�R�����'�����tG����f�FFwE�����K0:�%P����%�	Z�w�{����Y݊�;W�]7��� )D����҅�@W��CgB`�s-�2�W'�+���������_�_,�I����IA%Ry�^���|��5Iņ����?��k����X�X{�U���Τ��)M��|U}���x���t�_����\�m�K�ݗ��D�V� ���B�f��ҴO���R�>tS����w�ډ�sW���*�~���m�tb����V�ɹHIɟl�NT6>-��&����f���"lՐ`���5t������߾��X�C�V)R	���I�k�l�����d�;l��@�d�E6'�rS������s����zw�Y�Ȩ�v�-�=��%�^��ˠ%k�^B*M�U�D�V���R�H�I9�,,?qÑD�q/Mn����7�Ӷ��f.,aF�&ȁ\ղ�h�rZQr>�C���M�~ @F�H��⧕��N"�j�9:����Y{�w��[O/c�?q$�Afc>Q�i��贲 kA���q�%��b�l-���~ȇ�ۣ$���h�ڸU�uDY;�M^e;���-�O���Lo����zA�`_V���Io24�{cm�^G�i~��%����X�M�����?���P��@�Bҙ�m�����Ӆ��E�u�B�)�(^�y媦�ۗ
J��1�v�7�O�72��"�!���{��bϛ�D:��-9]��ޱei�c�k�4X��M�gc���+ ���V�ݿ��n�� ��4��s��(!����ب��̀=#����)_S)�֠�\	F�$� Ǉ�u �I��~SEP�4S�4l�8���tN٭����V�Av]- =e�2(7���HaX���D�*���{��9��NM�޶P�������[�]�ΐ��5����!}�?��+�A&�����Yu,�M�tX��{��:)�CPDq7m�o�XĩXd��P�a�u����;o�g)��Š&���&�S��cܭ�n��c�[�L]��98�A
�T�_�����I���Y?8�Q�o5QxZ%J�&��$5	�2��;���c�w����N�+���1���c[w�k�{��7V/]���liiU�	pwt�W4f�3���	�}�pry��&4��+k�Y?�,�F�����mmY�iWn0Wy7|�R1�,���Z6���Uww����l���<��n��,K��'t0#!"�ʟY�KK��l�K̀/��]b��J�Ö
��U�s���ѱZX��QX�!�.ԑT�s	��{V�c�.�·#gS�3��ƺf�cpyި�wv:==N��<�9L��?�Q�|�쉎���{
�z�S�O�_s@�:눨�f����'�6#�[<���H��x �=w�ō�l��n�AGݖ�,%b�)�U����@D���Of�Y"D��e�t�6s�����$n���b�d0����4�hJx[���r�	'3硍��^�ǁ�W�+c`a��8�:Af>���Y����ѵg=�]ӄ��zE)�x	_!�FCM���i8����j��d�:��fZ�D����F���%���c���?䝭�#�o{�
�L�v��²K��h����b/txJ��F�[O�z���'�.X���Q���m�?��:�]΄bv���ĥ�X�{�4���f����>׃��F�o�oO��?�D�'���`��ۇĖ,lu��֊6�).�W��:p�_� �V?���ޫz!W��q�ϳ&%��zy'e�W�:�o�^�Ƕ�$(�[e]~�%u$G� �k��1%���g'p��(T��b:�����1Ư7,DԀ�q+�0�Z ���:��<��=������n�Jl�]�P/�� ^2�/(7��&=%-����OߺV��2�y��q�:-Ɗ쓎$y*�a�	l#��ŭ��r��;D���a{��Њƹ�>���Zq�k���Z��d椀��S��\g�ԑ`�#�����7�ˆ�Ѕ#ѠP�"�=y���j�H+��|B� 9�'x�Ӎ��＞rDm[S�|:?�g�Mwˁs9�ǘ�q��X��ic��l�����:��� ��]�&P&���gY�����[xL�����^�+s�����eW���3{�6�_�6���7�w�7��b"��x1�P�H*&'�N�y��h�3`���D�s�s�8��	���-�_6)�\��+�d����M��O�/��y�s��i��)�d�6#�.�E03�d����nխ${z�8�k�5��w>�Z��"��`��!�1{e27��*` ����ȍ�|�b��ג��'�O#��w������5�K$m��2���!��C��������
������9t�<��[����uÇ����ɋ���>޴�9m�x��?n�q�x�^�0�
b�r���U��F{�lKl�ʢA�W���^c3}�m^,g}��2+Ʀw�ːG���*u�P��n�o�F�9C�.��>OWW0��@�2#j���V�YD5�z��l"�e�F&7Y�[~豊�����p�V�c�>��M��t�=!؇h�`D�4��"�Ov�E��{،�J������}8n����u�h*+N#t�p������a�w3!pv�*���m*�7ܫ��{=j�_�z��aI�1g#*A����8mux��2�s�BTV��}����J�:<A	�@[�W%5E��n;���A����T����O�bϕ�v@�Q�͆���=�JW�X�_j�)I�&��ҏ�ܠ�2����1PoZÕ��s�=n�o�lo�I�w���]0̝��k�p�H�1��u�����rߖXE�"����5K��"�`���`d~)�%>+��C���}F��>��&�<��cAt���20��>~�vXF43�� |����)}A�VX}��~�)퀷7G�&">3�ɕ���=�2y��S��׃��6��<'��j������c��2DmTks	� 55)�K�2���d�TZ�o]Rp�R0�!	��Q15X�3�aB���r���nf�W�C�� Q/{��Hn�i9c��r�t�Y3��.�y��V���L��ڒ6�|Csn���d�f�Q��fk7�8(.%�wfJ�~i����j�7�J[�/2���Q��|�����V�Ϡ�^iϻ�vOڵ𫹍�D?�V��<�(8仈�0(x"�l���?���o���Ձ�'��X�I�p��N�If�e���/zV�51vͻ���ۤn���{#�2U6�Qqj|��O�t"=��_�D��w�o��(�mL*��Q���H�.���U��n�^��"�'%����s��Hh�6E���B�u��NN��w}���Rt�#bʅW[�*�M�.���3a��+'�%v�E��m;'\���Nk�!�<�ʫk�涉��u���]'�fw���pIЍ���U��cЉ��%OI��P�y��� � ���3�4�)��ܦG�-xO\���3�{2�p�^0�肗��ڕF/6�tc��}�^�������cԤ�����Ӯ&"Ј�ƾ���UE�#�N ŋ�T�7q���i���A�g�˺���`��9,tp���'Z�=��c����{>��6Od�2`hC+BDr`����͹�v�%y^ԙ��n<���Bf�Y��G��������K�u ���}������Gw�}�����s'�\�g������b�O&_��;�1�LC}o/ar��8l��y-��h�s9vŅ	9� ������{��k����c A���~�,)��z�L~o�V��'�Hk�ޙ2~Q씐��OЧK�Kgr�����K���P����;�7tfH�����Dw^���ߊ�N�f�Ѯ�� $��t��C�`�W�V-9j��d��uv�y���b�<����k��wYa�Ȏn�e��E҉�Eؤ�����w�=����
�9&Q,\�*T�(g$�e[cb=�+u��n��������e�^,�g}����A��s���e;�?M{6�~5���j�
1.�� im6����?��+��]d�I۔(�g�O;K�V�,�����F��ZZ��I�1j��M���/���d�<OL�&�q�ǬT�s��S�.� GR��R-7v��n�4-�����蘞�<g�9@j��J��V��{�/1��l&�#�0b /�����@U���u����ď_Ī�yݏw޸�8��a��p"")��YJ�B�-v�D�e%�AW�Ҝ@J�j9��N�ߐ�M1H�"�7Q.����\ZG�6d�D�ݜ)]���౶!/�¡�O����rM�	�l7Ntc�;*�	�2�E��G�n�M��M)?3����U5��e�7�늎=��5��C
�~�)��K"��!���Sy���+���c"6O\�b�+�� ��K�M�q��_�#�%Xhf��<$_/�v��6͔�U��9z*_�<E���U{�J���������#><�0����-푚�t.y�XLQJ��r,�.x~�,����"����q���B�eAI'�a�]��~�?�9�)~����,O���A�x���1\W�\m�a3��_N)��iʉ��.Ӓɣ���w�
�[�l-��i�
 �Bh�2�O���">��&��̦�������̇n��6*���_BP���Ziju%�q�rGb��y���W}sG�|�F�%�zrx�a�d�\���������<�T�F��~�2m��#��4/^%���y(y��>��O�F�u��x������������ɇލO6��,�Ҳ��ҏQ��+\Y������4	���6��\�Ʈ�ě΂f�V����Fѳ٧V m���:�iX�8�@���+k�\U\�|K'��&�<�����r�wyO�fH�2[rs�W(f��]@���J
#C|Tw�r�֩Z`?h�vU֫���\�;�8&(R���:g�;޼o�>p�󵪃��߯�Z��y_wL�$�3�ܯ�;5�V$fd��m�����e*���$\�G\��M�k�����T�5lج1`�ɼc "#��mCͩ�^G��jӭis�ˮQ��y͙�������M���p
�_?�V��ʚ+G@�Hʟ���\
�{�*,"IS-�e�}����^)���B�8ɫ-���Ƭ����*�ev�5p���ȗKЙ�n�F;N��8�c`*��G&��Y����w��YR�lf�/�@fo�JXԝ�r��#��SL�%���&������q�笫X����y�{�2�X�Q�٨����Xκ���C�Q׋PӰnT7��Z� >��z��\���WGs�S��Q�w
|EoDK��1k1��a�8?@hߘӋ�W�Z�����.?&��p7��.�c`^W4G4Rc���qwNw`�lq���k�ZY"
	��i2�'���M��_!+²|��+��!�k�ߣ:3��C8�r�d)lମ� �T�u�`pbdj&7ڧ�h��WYc~�8�i�"�����d2��/���k�骧(
#�~�l��iFt�6����KW�M0� ���A��iU7�n�Pw�&mu!Vy�nا����"J]7�����Zr��T@޽t}�����ݹv	�v���Ǉ���D������$؀�h��$��W[��j��j)���j�o}������p�iw�z�e��y�t�P��:a#Ъl�|�����8�X��O���pȾ$7�|fXuo��a�0Qma���d UB��I�~%���d����WW8��|�gɗYlh�D�AG�6�����z7���ë�DU��;���(az�J'��#��}s����V�-�_���'��Zܨ�7dW]uR��� �!=Ћ�Yk`����z��#>���uf7���Ǔ�!�SP$�TM��3�Ӆ���`!
{&�}{�?sO�u7ʈ���:"-����Ie	L���cU���5��R��r�]�1n:>�����w]y�m?.h���������§��2�`˺��A��i0�j2���#'K!:�撫��s��Q�r�r����1���@-��V�\��b�9t�[B�7T�C<��V"&��ľ ��(�����Af����!�.ួ��xqi�=�߳���ڔ�P��Ij�5t�Ъ#�曋�c�1���G㥿��[��}��ًM�+8b�3����atڂE�4��c���<��������JF�A��tE���W���[ީz=]л���o<�,?��h��U�Cw��ĵ|��n[���>�]�/>b_u�^H��Ͱ���Ws�48T�\���sU���`���F���o��1i����ʄ����OU��\�j�5"�������5���X��g\Y�F����!�j��3�x�aU9�e��T��`)��n������"���٘�!��ߘofE�E��.1s�����Kj�s�P	���)b5���Iʴ~H״{N�����$�4Ѫ�N��&�9�^ʾ�����iںE���0�},=>|R���1=܎���O̀�ޒoW)I��f[�]T�
P�3�8��)��x��$L�=>rm���!�!�UT&uX�;�7z�1��1׾>M �6ݟV����`2N/��������HD�~W���*v6h	p=���+Nr������n5|OXUtQ
���H.ApbiL΃g%Ȣpc\߀����_��r��%�+3�N�{γy��^r��t��r��ʻ�p{����Rx#*���.��6����!���׀8R|;�U��@���*��b��'��=;6c�_�^���{�R�7_�yJu��xW�<�A���h�W����}����	)�}�.�4����4��A�B8YNPi�7F��i���n�c��E�H�0�./�έ�����<���*Q���xV�Lk_p+���������y���[%���$�ʳ�H�䁮��Y�.��^�i ��)fR�R�3�58���4.b���A��33�y=O|��Wy'e�$-�$�*�aK��ֿeK�Y������ �����A�%�k_ufw0���Ñ�WB��K�I��L������P��q��+�)��^���+N��,��߉Lyw��h�Z�)��M��ak�Ms��@WI���]����j��"vS�J@j���wՊA���E_��n��?RE�l�sUS4U!ͣa�!���NH�˨%:bf�G ��~�'�
���T�λ���bt�9��b9(�=���X��5M��8}�T�x�W췐��D&�&�O垼�T�:��׬̺{MZ4�܁��8�q� �Z�7Ԍ-6j�a��EJB���)j��8���|������F��G��o�@�������a˞�ei1s~�;�%�|i������<+|4��IѶ����I�!"����j�F��e�=gcSL	g��uA��Q)er�����ӳ���p]��[Ix�j����z�Y*b8���,���l@��C�>4�[��C~ɨ�5��i����[k��ɲxk�(���c�.".�,��-��@�:�o�Ṡ1���GK�4N�%�($��eª���Aπl-�����¥��w��d��К�CX�Pg�f2Dd�NU�wX�B��$E5�,q8�yy±R��2��"f�ם3�}�t�c먃R�Z�H��S�g/�H�������_�-,2�xǧK�_DO���4�h<5Ž�US���\{��ʌQ*9�8���4Kf��SB��ב��=?)%9����I�� 74���d��.@wU��x�� IGG4�4���ɷQK�W�����B�v�
h�#M�݇�����ϋ�lF+M��u%�"F����+k匜�c&�8����0��;�+�cc�9�2�w<]n�s���Zdc�!$=B4��R��S���7�_�z�g���=U#F&���q���5�U����{b��ע���iN�����,,��䨧���ȅg$�;�����t�
����l蔧PK��V��g��>.�o����ՠ�����kG֎�6cLMTx�f�]�;�Ѹ���_�"I�T�g���/���1��G�F�x샥ge�w�{�����O�F�b(~ҋ���hأqֱ<$�}�[H~AٽmO�{2�vvF,5�)QC��k�W���*(F2���,�\��:�`עw2$�%���bVqL#�l����B��#G}�t�"�p�Cy��m�M��<�J�}X_G��bdJ���0����4V�[����>̉�./4�Z�p�C��O�N��ǈ�]��کK�kh�,+ze��zKG�8����yj�|,���|U��d)��o6c-JR��#^��Jܔ�5��RD�5 [�!�3~Ti�S�LtJ9�+����_:�#��/)<x��
,<`��
�$N[��t�o���ns�8&\���N�ݙnn�y�� �<���o3�H	��m&}�m��a�1�x�~vU���Q�j�mr��zN�s�ۗZilQ��V�w�|\���6\}9�R<h�ڄk��Q/�Ū㪙��͕�ӽ��f�/��Q�^��$��^b��
�_�~�sA��x�O�Gq%3 K�[�]�+�̨��������g3@=�Qj*� }��N�.FX2p�V�:��^ґD��F7���>��%�!�Ʈ897��q���M�8G�����͏2S��2��B�f�nb,�8TI�QWz�W2A��^t1΢�m�^�u����=T��{tCMo��"��5�l�E����&_=�-�6tt��M��93��O���-�l3��R$��	�f��hO4��C>~x��ώ0��91�Qm��[���SR�u�*ڙH{�{z��ا�7�8����04�&N��a�}i^)���B�LyEl�ƨ�:�M�K���㥇�1h���N4�>�QWf���3V`��-f�*�ӳ�L6 ��%Pi��KAy�x0v��p��W�>\�<�{X�)�2��f����U�6q:�nY>�*R�ܦr݋���LRE݂�l~E�{�gx�$n���]��Z�,��u��ZWȹ&EO�X_Rx���WtxM��l�/�(�|�PLC�}����O��v��e��a�G	�4>�W�B�@h{ܞ��O�lE]�ֳ�m�e��ž|mh\��@rӕ�i���?��ǉm=��b��xl&�HnD���^��������}Y0��Ҙ�����Z\^�TD��PK^�@��  � PK  �@�U               word/media/image2.png̺eT\Q�-�	n�[p�&Ep��%@p�.�Ca�K��+��ݭp
�����������������㬽�9k�=��+LEI�%&�'O^��|R{��)��7�����L���j�O5<ҏ�P�'�����������D?�0�O�--}�D�*�D��	dY�G*�*T�"�}����{���	X	h2���}���x��t���熻	59�Q��@�q�8��tÄ+�_"z6�Nv���
ɼ2g�ET�|�$h�n�<�?�?R�z�z�����5&������>�AЋ��
<���U61���Nb@Eҋ�'w,�-x;�;�mV�S�J$���d���g��2BY&�xÓ�K��F�J-j&(���/U7�R��&��!�u���c��D�ȴ��\��~~���e���u�X�g�!K	,ţ��j�Z��|ʒ��4!謁�-�D���!C4@��T��!<ꍼr��Q�|ä����+�Wϖ���[f2��l$n)�}J�K�j��N�kj��W�.�����S�T��n��^:�9Y�T���&�G����e���@��=�$�1��?��ϲ����.�
��@�f��#�mB��N6|
�	�Ύ����q
&���%<��5F���$q�)�L�*T�no���Znpޑ}�<]�фsm��l`��w��Z2"/ǣ(Q>|�n��b����ب��Z�f���k�sA���E$�7�]��h������w4�#O��+?�7��z%�m�h���z���;;�X"�W
�y�Pd���r ��H���k&�76e���,-�d$|�6�Rc|�D��W:�枞^^D���e)x����`�a������II3����\I�����b�S�Ej�F�#���pb�*��/�����r0]6_e6p�g���^k�|��$�h�c�J�;��m�����|;���=������'�垑q�`����c����j�Qjg<@�Ğ��5l��녺�į5h�T����'ڏ_�
E�T~1N}A�ϥ[UD&��VR�Z����S6�KD��ݵW4�ub������&\w�G�Ђ���n��F���uTL�r%���5�`\�����@��
>@J ��PM��1��?�hH���_� �v)�C,7���O0Z��;::X^0�<�?3�/tp�Os���M�?�F���ihhC^P�E�v��~V��:�k^R�N���r��J<{��O!RZ*Vy�0e��W�ƩP�A�4S̰Y��s��^`�b�uμK#���㑻�O�U��}�dC]P.�٠I��E� ��Wϗ���qlD���.�/>!D��y3��̶ph?������݌LE����!(�p�r@�E�_��x5!�LK���A��\ǒ��E���b��;G�,��!�o����r��tIk��v&�Y	E�nu���]m=Ⱥ$�F�,�F�FR�SDèGDߞ�a-[N%뚵3K�-��e�N��� �X�n��^askR�I���vu�vs��w�l�����H_�C
�r�@�C�)B(˦'�}�p�hp�[�?�:���k��b�rfQ���P$�5�`H���?���ޞ�Ye��C�-}�D�Ҡ�%�y������`4d{0��Y=��8��W�P�z��� ���.���n1mpG��\δ�Y�:'����i�Tx|�@u�2�N�� b�ݜO��>�h6��d n���<��8q�L��;4FH�Ǘ(�Q���iv;�|�G���Y��!�	�C1tDλ�`|��&IQ�˛-q �]
��/�r�Y�2!B|;o�̾����SD��JV��80�.d�,E���]Π��h���u3dE�ޒ��_``ٔ��KS�DRWGe{f��W ìI뛙����k_NY���D��]��I�qM5r�/d`�<�᱘m�`�n���4�$�Ճ>L	�;lj�7�����Zop�S����G��>_Fm��6�}lF��AN�_�%V�8O�h��K��Ή��(��lf5�9>?U��t�\�u�~�L�;�eP-�JBX�%����鰽N_���b�%Q��׊�8�)���������oz"�����\�B����%���|;z��V�>�n��󻋈�c�w.�O��5�L?&1��xym��%:�=Zv���Z%�`��h�Z�4���Ʈ6w�s���i�$��|���&wUf�BW�+y��Rv�����P-e 4��U�g�N}�kd�Gl�����L?�Sxb�ʥ��t��E�7a��m�Qr��m�ˀe�">:��	e?�	���xp̐@��`!Z�B8�����)x�6m\XI��f�_&������`�<1Z/�c�����`Uĸ��>�4��-�X0�X�x��EX��@F��A���t��}q�)�:�[�7qPS��3-�� �}�W����z�ڪ4)��{�߈n���.�\��3��z����j\a��-��$!$�l(��{�w����SPK�Cn~��Š-lN?�|,��G��H�n ��K�<�P泽U��^�\�.�֏��0,�Fo}��N�q�U�6'z�k0劒�ֻ�c�u��W�CC�s�c�#=�B�v�*�
m���N��Om���K�̒҄F|��+T�;�ڡ��Z�F�
���.�K�����d�qk�q����Ik�u�[K=����b?���ؑ�fp�����;|���+Ƥ��]�q؏��J���h�����V�Α˫�O��x�'
��4��P��|Z�`���<XW��P �Z�?��nԶ���e�H���F�^`�bu �y'�
+3�2����q��3�P��J)���
�L�+�Vͷk�o 3��ǳ7��\�V�	�*�u"JW�02�k2���䰮�c`k{ę
G��N2�޽x�*�z.r�\�qk>˭�"5����by혜���GO:)��%�-�pTl�`�JS�p"�闹�p��6��}d�\�����!G��Z��l�c�=�
�6fC��B=���X&�Pg���O�Pī7�Xn@�.Ro��_3+�f�ө�� �'�䫎���#���_L��,��\5��%1�ja|_X�P]�D��֕J��8nu|R���Il>�00Ή_ق�=_11{Pa�{A�+T�v\g��)��Ц3d���Ժι2��5K�a}d��9s�:O��gA��7`6EP����� �wX"\�͔���ҩ_���`$�=�����4q�`�X#�+��p���0��T�J�I,��[���B<TZ���Sŋ]^���B����F���:['��pJ{Gt̳>��|�Z����tH���
��3���У�x�}q@J�<݊��լ�k�j���Gl�,8���2�U��J>	)�����p|�"d�U�{!�nq�P����u�x�B{�ʢ�T���|��*�3� ��I����p��ZCG��$�鄁7����m|}鋀�#��w�Y���d��:/��v�"�j��J(7Jig�(��'���5����	T��h
p�5����������-����u��=A��#ȵ3����P7���]����Pl>�k�3�i�R��i�M(��|2��}�_Jwb�76�J`l����cT���"�����z�ȕ?�:�UMz2�)�_���6O�&|�	\g�.*Zۀ��u��	π��|>���_��W����`9���`j�����}���Y��X	)'W>_d��[�~�&��O�z��,8����ΌN����B�Au�an�8~��8��:E�y]7c�~(H��'\��P�xx��7��C[`9*)\�ù�k���8��7m�As.;X5���f�t��'�\�c��-�E��T����Le����!�)��U4���8&-�<��6t.���SN��x�xZ�b�l_FEJʡH*S��n����d�2��u�,�X�-p8Q�׫���%j�c�����-<�k�2�[;Z��,�\�F�`���x~#�t�,�J��S���myz��9�^�*p8�2ưv&�TF�F"�م��|R�����ҩ��f�l��/�k�?�O$�ކ��\f�U��:nj���$�؏�V�rJ��,Fe�nV�C<ϯ�(W�8 VC5�����Ae��]��lS�%k�c�U�_u�bm��Oy�;���+�0�X4d��͍�ɜ�8��b�U�u�������]��QU�^��`���s�T3F붉T�`/����c�2��@ݎ�u��?������:�۟?/�f:�����Eo1��o�t��Zm_J����:Sf���x3�'͗i����#�Y��j�*��}.��c����gbE�Fj�
��ă�`���� LBlç1߄�k�L��� �a�׃}+��Sё�v���g�^��CՌ"��?4z���JC�+׎a�����E��&0�{D q'�������֩��c��`J�LD�x?��7�1;��=C.ҷ�{�]+G5�La�9�4m�§��%�m,�m,���o���B���)�ܻ����k���d����UQ��H�Yl*/-�Ǘ�b[���W��z�T{9�T2ӌ�p��n�.}��4.1ya�t�/���zD��u���{3�x���3�?�QdL����7��HJ�5��T%�z�ƻ-m�
 �Vm$RW��m��cl�?��]�F���P8�ZtM�VJW?����0�a��cH�t���:�t������2m5�"���jvD�7�=�[g����g`��L�%C��RS}�=�F-�](&�4��ڼ���۳�u���'\sH�ƴݺ�J]-M8	�ޒ����}-Jm�t�����K����N�ߞ�J�S�n��x�b]�ܒy}cQ?�{G��-Tc̏XW��fk:!8�lO����C��{�*�ro������Dų��)���)�s�qM�N�_�/fN(��Fe�zL���B�	�Fɦ;_�Ɯ�۳_���T�W���Z�r5�+�j�/���gKo2��~d�{O�c�����_�n�E����E&��:7Z��_jǍ�uJ<�Q���>��G8uG�;�4)�R\���c�m� 	��{L]���d4u���@>d����2r~�Ӣd\4�U����	*5����5���H$��os�Y����z�I��]�߈��i�H�:��}&a��W[���mbO�l�@�����:�ڽ�� _N��s�+���}J�	`m��4�#��5yz�9��nR DJ�1�?<�կ�9�7>������f�Ɵ�V[�"������8����ל����y��rf��7N����lh+�b��Ki����%�D���I_�1��	�f̃X�L�F��&�4r��\GN��/W�Y�L' �Q*.���R���\���k+\9$�sD%�/����ʀ�せ�J�z��P�HSp[OTNdKG�VR�J?x��H�j��ғ��|q�e�ӣz��I������d��sF���
��O>�,G6�*m�,�^F�uؑ"С4#�ʗ���#V*�N8M��$��r�^�	/$n ��3</|m��Ǵ�)4 ����C�^F#��n�}�,��ߓ.CH���x�{z��`j8����6���<%u�g���R@�;����
2%��,*�!v�yI��,e�Nn�J���O��a,�M�AQ�_��Q�u�}z��t?����Gk6���`��ޥ y��%�~�1���L}��cOX��h^4�0�+�b�b�A5�NcB|`����?b��} ^XR�|q �'� �-���7$�&��nat�.���yY�<�=c/�&0T���rw���GH�*�����F-Q�K�\�)��F��< z��R��]@~|⿌�����X�d��<jz��I*��y��r4b]!�e�@�O?_��Ŭ:Δ�'q��J��.N������u����q���d��%:,�^�P�(��P�?W�\je���B_��bß*��0)C��ܣe,d!`;�g�5��W8�L��m�S��l]:5,�"WwO�Yb�}��̘���AR^NFZ�$�\���!9p.�t��ӪJ��@��/���D]��7�k�r��b���A�*���)?<�0ZZ,�'A�X%Ƥ\�W�w�YN+�����hѹ�������J�\*�x/Ԋ�p�Z����5aQ�O!��19I� ������֪p^��g�ʳ���`�D�m������ë����eIa���y���K���:!'re�=��G��W|��2֮���w�/q�S��R	�s$#���Jl�6�{͚�#?D�Vr�
�!��Y\����P�l��\��{�+��w&�=��l^�^�u@��0>Kl�R�7^�W����8�J+���X���|��醄�3uU��L�v9x�"��Sǅ�t����l"#��s%_H}bN2�'�/��+Ġ���%/M�Ά7A���
q�s�n�$��$[�ë2�E	<�����G�-׽��)+�1X[|%����flJW���:����M`A(�3D�3���>����}�Iʐ�˽���!�x���̙WCG�����鹣S������p�\y���xD.��h��D�ـC�4���G�%�.�,=EU�F?� ̇�ro��:祿�_e�<�l�r���}w�Ξc�h�YX67~����!�U�f�X��G�s��1�-�ȝ��5� jĴ���v�ػ���t�N&����k�B��M�_L��K���s7��[�2k�5(F�+5�u�$Ƨ����Ei�0����iLV8U:`�ٚ"�Ο꽶��T�9Rr�d�B1�j����$E=x,���v���L�nExn��+�W��\�!��{@���7Ml��P	��D�� �m@kFv�0��G������
֌k�VS�y��G�t�����^Q�>�
�;~kp\�o�S+ȑ��������6;�~5�?U�0�&���Fth�$��������O;&�^�K��S\�}$����e�-�N�_ð^�&-�u:DM�J�(�8�^[df~V�H ���D���dY��3�k�>��qC��L��q�}��A�N�(9f�]�U�C��ԡ����J�Ҟiù����E~d��������-=�N�0�Pk���BZ���Oha�l��q�W����.,��bA��un��~��摬k&�_��	�+U�K�gj2�b��`��\9�CZx�0�ۢa�i}��,����3���ƽ�V�LI������U���:0E3)��h -~.�>�����U��i^'��@�x�sL�\����hP�	����r	c��ZL�f�KS%�t�WZ߉O���|�i:�����
����L�.��p�>���x���T����"�#09���Z)�;,���� wEqaa]j�X�_]�{���lqf��9�C��%'����Oχ�/zS#�fh_�T��eJ�XZ�B��F0�P=�M��O�o�����Un9�f�Tc�;}�� R�.�Mi�UA�7�*�����3����<��g�k�עt�O26��D:/T�䲜��X�ZZ��|� g=�2<� ��7�vv�O-	��iVIj����Z���Y�戛{�����6�Wr-g�X|`�����c��7X6(\P��'.n�^����:$����r/�U�4\o+q��z�7��L ��}L�\�L!½������v�������E�8�27�D�}�:ߙ{�}��N��&s�3�S��[��8���v��lw8��1=����<�)o)�����k�S�gY��n�R�ؕj����n�!�Ċ�(x����T8�������}��ga^��ܳIJ�_ԃL'�
��d����e��ƤS���r!B�j-T�*�,�6M
�;��3!z��7��ka��."K���i��<���u�S�s�&�a��Ҩ�<�2�N�В|�N�h�G���� �7��B�;���u��H������K�2�Icbܺ�YWr��V�)RĖط9i�'|��UZ����;����ᎎS�=�X����7��$�r{��I[�p����I�8uC��b��E�ן�T��6��eTB-��.VFJ��Ժ��e��j��ȭ6�}�J�f���yx�n>�N'�z}f�@�YF�����+^�cǟ�@t��G���k���+s���c�Z��+�jt;��Јe�g
���{�â ~��`��c��f�+͘�>|��:���}F�8��w���9o��b�7yRO�ӷ��x���I��hb���`�a�.4��̓����;o���A<ʨ"Ҷ�
��E�D7G���R�����c`�L�v�>��ih�|+�쿱���5L%�?2�&O!@퐉Q����
�w��N&`���51=TA ����ѝA,��8����.�+fiU���;�6���t���]��K�,�����;�~����"��N��w	�D�p�	����Z9E.�oRz���4qo5j믪6"��� �fէ�(�:��2�U��tIG������[��F�\�ڄ���8ȭ�Rw~׽ "���0a<�1�T��Uq30�f�;���>��{C׎�5�]ʟ��`�9{�������w�d^wA�*���e�1�;�zO��'���.-�%�BvS�����^��5����LWr[7�ZO���N����"�v�_,�E��Ұ��\\�9	P���V�D�ӿ��(�k];���|ۇ�*Ę�F�lr�A��n�	�������3/G�L�WPf�����-�ǿt��~r�w�_�����oF�]B.�jɉ��Z��jp9�o�.���,$F��=��T�X�Q���Ț��PS�e���|��[T�'�4S���8\������)-7{(�B(���<ah��usK���"�U�k:�[f��Yn�<��y�3H�Lv�]u�Ȯ����H<��f��wB�v��]�z��R��A]cɕ uK�7�[;"���v�	]�^�=%:&J�6
�d!9��?i3h���� �ݎ}y��:�@A��2��oU��H��U�����PI��-��tK�Z9��b"�ư���߼G����
�,�\�;�X��߲M�Ӟ�S Q��������w2cEu�1*�Ŗ���l2߿K�|\�lM��Բۀ��%�?�`{���lK�8a>�yG�݅��Oe�_EYt9
�rNa�����}V����ILc�
���8��,�����_�t����%ES�����1|�?ɨ6?[ҟ�Pa8�6��DLTL��,�f��*4�'���a�/m}u�}�[c���>��Wb�̊�-kӮ����a��h>[Oт3�w��.��P�]|�￙a��z��fL���ꆸ���k�q+d��g$$������aQ�<�G��*�{ay��|�YS��`&mqȈ��2H��;+j��o�!|�g��pS�����v��Y��)pPeT6_��+m�|���vn2��h�e�.JВ��ď)��E5��(t�
����ڌ�6�@N�8ТY��߷��0��9B��J�ȃ��~�ʇ��G�Tc�E�ʽ⌂��T*���Y6�7�˹z��1�z��a4���v��BԻ˞x�aⰸ:`���<9T�m ��.�L�a���"2�A�G
+�J���Op�k�3s�#��vGS>�����Q<��ޣ/1����H�b9`��-�E��A�&�^ t�&��;醸҉`�Ъ�~vH�%�H��2�jV���1Q�(�g��؞��I�>C.����j`8C�j�	����:����^�i�B�<�|,���������-^��8�K�2|���0� ��Ua3�<٨��Y�q_^o�s;5}r͡<[E�vBk[�୾�L|�t�5w����#�[A�L(�"`Ie������|m5�;�w0+��1���Q�y���V��`�s��a������X������{�%����WfW�\<���\��Z��Q6n
@|��Բ8���γ�cJm�����L�)AOi�^�iy&zW�>:{�p�b=�V�ިyb��/��O�'�k��^���

	���,y�_Ku�{�\ 1��M���\[lԑ7��>����\Y�yM���!��AD���o3B�����*�OǇ��|��h[<VL!� *�����g����=g%�!1RLY7ʗɸ�cŤ�n��O?t�&�15Z/��1�45��S�ou�|Ӫᛄ��I����~a�[�����1_ႊj���+'�.�8�)���m�O��s�:MGY�p����*v̜M���J�j�[g���B5hh�՝��e1i�"�
����Ɵ1��,�{��Qt��B� �	g�a��,˱w�0�_���ϢX��Ktt�c�@W}���@��j,��-�+ڵ<�8A�Y�~��O<؄����vX�d���ģ����߈#k9</Љ.�g���Q�P��m�("�[�S�i�E����t�K*�;�rt�M�-��*z?��by����sv���tbh{�K.���=5������h0�C��V���P|�/�=fr�SRz�ɲ�ړhe�i��Ȇ)��&3�Jm��X9�B��Z��N�s��J#^�����������տ��R�=�f^��+ۣ~�A��xh�A6�˄���5���}FE 8��ꑱ6<@8��_���t�*|�K�X�`�L�zD_��7/��_���Pv���ǻ�2ei�����5M�ep'Y��N ��L3�ޮr���Y�{a�{�ٵ��`����Û;�����ϧ��!�z˓[g����p_K�m;v�r�?y�N�����{��(ţ��_牪Uu���$��"�)���܊�3�f�c� q��ÜH������PR�`L�>n����p�L;ؕJo�)���A��F���>nJ�(��I�<���{Y�l�R���:�_�x��Xk��)�-�R�������"E�`�|f+E�HP��s��k#@�׸iǋ�d{��^�ه�C9�/�5�	J��?m�Z�GV�n(�+%1�"���fsW���d�����K��,���%Rd�'���@�=�#��]j�����;Z���9��^����Ӝ����!*3m`��F�%�B��݁���������'_梉�x.�7;�#gy_�ơѝ���[���۟�W��������F���QIB��8�Cx�¼�Q�&���>����Ň�ܨ�M|������;í�H�p��$�~U�c|�!ف#� +'���7x`M�)�u�^�Wq�!��u���O�Qd5ę�ڒ���Ǹ���t��¯zI�J,���U�*�yJz��W.�	�_���f�[sg�Wf��e{ ����er�I_n��Z�!�/��jj�k��1�s?�zn�}�p�A�j�Di��Dxs���}O���J�#80�\%6[׽��]>�mb$*Ή���k���kdA�����(�{�d�m|V{0�W��֩��_Җc|���N���9ی�p%3���a�:*�(���X<quV��z&�8������A�B�&�~޺�y�_��x=ߓ,0�3v�(�#a��AT�Y71n>�ԟ�b�n����~���S���>S??*-���W���X�ߏ�����f��u!���C�+�uu�s����?0z�����>�@:��V�&m{�xQ�z��S#�O��_f�h��xq�N�H�M�U�x�	6m��G��2�~ߍ !K:�.�=|ݐ?o����ϡ�_�F�)�D��W�LW�N,�gϞ��T(=5�L~Q�=j�9A��,�Kx7���W�R#d�a�v*S���ރ2͝o/Z�y�g��2Y��ZJs`]ZP�M`��x�;�#�s�l�^��(�N���S|�|k����64�O*�G8���\���&`�o�Cn�L0�(1��\���Q��g��z�lwęY�h�ؗ����
������4�L̿+ � ��dV�B ��Ē��=_�躥T�zOu�
A@x���9a��5{��#�#@[Т_�Թ|{ʼin�*��<�<�P�2��&2�TT����'�ʲ�62{>����g�6�7֥ Z�0���R���#u��㪫e	�.�$����̴�����Iw܃��`����p>��u�r�w�F�jϓ�=02Pݶ�5H��rj��j	E���=��Z2k���!Q�'��k`����5ƓZwA竧Q��L�߬�-4`ܻ�����SD8p��Bs8�'���8���;�l=�!���HMWo��.��w���`t*@� [ �����1w__�h*���j��I�Rk�2f��d+�;�:�dȕ�V�"������A��[�6�RD\�d�S�Jy�s�8��䘟�@��٧�9��|���sN�⥏���v�rJ!x� �K����գm&���d�ugOK�~�C���6�KB��f�C�á�k��[a3ݕ��QÊ��7սa�����]Ý����E�<s
����Z�ooV��SU::i.��)*�s,h���O�V�u"YL���E�j��%��������3e�|.����$�X�=!�$�Ztò�ѩ�W#�-�6�m�/6x��$�g�wk���x!���DkǗ����V5|�Í�&�UpK�9�?[��]�)��1���0a�pR��;��6ю�0��=QPj[�%�����1c�8�Z4�� `��Hc���ō��gM���"�#yB2vYxn���L�7��Z�#<{J7�+���Y4�\I��x�do��g�8d�\�ÆP�S	6����k�1��FTxm0�k��s�s�|�MK��sM��3e7~"�f+g�}�%��\���_�szŒZk��ͥ�q�4�e�K�~0b������$q"��G���C����KS4��s'p�K�R���}�MV�*Ȑ´��8NJV�ཤZ��ث[�{���y��A)A=�E�뭒�6(� be��M�Y>�vu��X�s���[�Y�lپog�{wJO���m�yn��NyNqْ�"��#���]����m��`<Z�G��J��o]v����&�Gt��N���O�����������=�qm���6(�?�����
!-D��#A�P�����Ь^���{�!����*�(�W��^��л��1d��I��L��� ���M{��g/�H��	��	���5K�2U|�AC��$�;ԅ�lW��-s�t�4����@E�Y�zy��߁٘�Y<s���j���y]��F@�����V��?O~p�t��3��Y�z'�D!��m�*2��zJ��_���FA�d��Ɩ��Z���T �?�}o����tZ��C���L�ζ�j^�
%��#��F���7��2�8��KV/ t�c�E�n��j\K�����/Xj�j���2R��7�I��KP�Ǡ/<��Ȃ���rgY����p&�2*�F�o����'l�?:�"k�#,������E�mwS9��i'vٹ���W��S�V5��p왔���k�Z���!�Yj{�9�{�z��Y�LU�P.ɔe�}%�;:��S����0���@`�y�tAr��񵲩�sƛǣ�'����6a�ǳ��Xۇ�;���( ���"޾���F���7��jŋIK����b!��B�d�ঢ়��:N��A��v�O�N����'���D��UL�f�Oqi�4�Q��~Z�
谵�w��)�m����*�t� �O��t/9>8��-�$!�￡�VA���������O	ӕ㶒tˆU�r��zng�i#5��4!�A�YB�S
%b�:Km�OیEF�Ğw�{���^!�o���U-̇L'��t���\�&$�9�;��4$��j�wE\Ӭ�=<�n��|����(��z���q �%exB�fnzx\��V�1t#���D���?P��3�+���:zl���%��aHȁڧ\d�Bd}�}�ᘨ@x[�AZ<�������@�1����̠�u���O�E��H�5�d'Xo?��<^�e�������ƈO^�x���o�b����YrN���r��4��uQ����z����D��E�G�L} �M8?�m��eA�mG����d5ag>nޏ2�""�@�>����O����-�v82�����g�A���D����Jy���f�$�RC�h��}��ջZ�D�4��h���[ĺ]f��z�޻m��oi �u���Ŋ1��68�v�ch@8^�yc�:�$8� ڑn6��T#���W�/���ߘ���tMi���>Ǯ�e��X��C(p_|�_u�8����"ə�ڔ?n*���m^��еM!]�=��E �?�4^0c���`*R���_�'�[�5�g��~md8����>�>��cN!&� 0���|O|�f�p�P�^���f;Ѣ�l���,sC>58E�Wj�0��喁QR>)۶;��a������������e�d��!o�����ҭy��q(V{+������<�3�pq���Y���W��<�9	+��gX$��r�a�����6j��^�6�Ĭ��L�;o�:6/o�*�Y��U{�]�X
�޹9״�,Ρh��V�V�|tP;0��|u������LFӍ��o��qg��
�	��99�xw`*;�q���)�����eh���`�{��څ�{�.�[��Q3X�ΓU^.���[�:�̗*�4Y?NI�+7����R��r<L$�?�g�(��F���ũL-JA�����G:zb���ݢQ@۞����N��y�s�6�����9�ZvrL�����;�«�wS��+��)G�Lk�dN�z�Gu�nCj��*��P�a��z�:�E4K��-3O��V��>%��}��ĥ�s�����oA�,�KP��D��o�UT�ʎ�ؑ$�F�g�O��
�^q{���x�x]�tgW�����8N@��.bNƊE3�sB*�X�~��E���P�o���`-z�"`�}�����U���A5f{#�ـb#�<��(ga�E�˱3.9�t��v;;�r��53�(�b����L���F !r�������Ǿs*k��]��K���&��w\�n���_[�d�E�{���j��(Vw�'���Hۓ�H���Ϯt�o�A����>s�ien���1��5Z۰C`�X�ƶ`#�{���h��w}|p�f/�����y����r��fST��FKC�6�a�~]�9� �]�w��2|�H��v�O�E~V�.c�I;7��	Rs:[����6{+�l�8��K�	�4P1�ԍW~�R�a�4��ϛ�n'�jȧpʔ���t�u]D�R7�.R�KBFkU�)��s!�Q��)���<)��G��V��Ԍ�mK��k��E�d�!KtC�B�/[���ՕN����sWK7*�I�3{	��5~)(u�#8n˲5���������ه_܈F�\���`��C)�|u�bE�ي��D82˥����w�����ۇ��r�C^���g��><�]���yZ 9�죪'+Ը�z�����\4��V\m���f6�������73F&��If�Ǔ}�yXD�O���P�����D(�ņ��S=eõ�p�!�j%�nZ�z:�ܰŘc\T7�Q�e[J�lSq(��r�A~ūɒF�M����_UqYc)Q+�ΉV��s:�I���9����]�ԍ���#=�2��2[)U2��-^�M��5�R���nj��1$z�m�>�_������K��<b#�"�x�M�"�H�*�8��f�V���omxe	�F��q�L%r7���YU)�O�\���E�1�?���N4]�����_���Kj����.�|-���0�@H����\0�U�_���-q�C7&�IȾ�O�hm�F��^�*]~s#��8��Mu������`�ÚR��ʪv�}Y΅zlђU���<����m�Hb���i�"���[;�a�FS�n"��������v�0�y�A�6x�JV�*6rJz�%?ɑ��wwc����ɛ-���V=�,^�n�p��wOȜ��ЖB�]��2��V+�{�
wPvv��W[�-�h��d\H����&�&/��ԗK&�+c?�F2�2��.�d|w&Z�.(�r]bJ!�
aH�Y�	B��bLzۄd��L�΄~�S>6���9Q�v�-n�	�%J��W�	�k��lَY�r쾖G��X��.��A>��+�
���$pK<O^WM/�#R;Z�&�5ض����h�A���M��g��C��q��Cd�̑���"��������� b@����]ȭ@<ږ3K�Β/�E���	��zW²g7ƟSy�7N�d�/��s�y����X�+Cp�@��J��%��xa�����ޏ�1���L���f�a�e����vr�ÞJ�|^��iGRU�^�1�I6o�.��.o��@Zi�Դ���P�g�G3ҍ�
��e]�X1Z�]��{�S���〯w�LN��K��>�}�S�]t�hFp��֘i�����Ӫ%:�����јb�Q�sz��!ɌZl3��.�k��{������4�X��}8��D�y���8�%ZL�U/��2�E)L�n#(�b����>�9F��5�.�s?w�}����i<c�ҥ ���X?tOV�D�:1��V�	�%H����}��ȯ��	����
kj�ְ�B"Ho�z���;�c(A��;�EG)�{���t�Ch�7	 z�9�{���G�y��9�����|���o|�{�_��]uM�n�K� �7��_�|���]�&�H�6�#>G3��Ȟ�m7���������)����-q���[�@X*�Pc��IO܏�2�t-�"R�(1l\Co����Wz΄U"94���c0�M�ND��A�����yì�k5��פ�X_�p���@>�'d{ʝŒQ�wdn	�*�0����!��/���'���ϔ��.���$̋޹�����n�W��L����ӯ�=\1�۴�8:$��9jU5��^{E��R�7Ҟ\�mz���sD�k8?����#�AJ��b�����t�c�J�s�1l�/�:��:(�,#sj�����Գ�!J`2C�6��b������@��1��Qz�J��`ߴ�C�am��ն�N�'�{έY
��6�R.��m/�r��1ԣ�CbQ1���C8�t~�L���]����w��)mCY��e���pX�;�cR�*"��^UeԁidSU�a�	쀷��S��[���©��!�J�BD��@�z��|���8��ӑ8lZ���W@�Eƺ#�>ln;�k���ۨ~�s���ƌ�	m��������b�Et��`K멹-%r��Q~�
V��ղ&u?�Ȋ
�GE(�Zh�G��W��FYtf��0�f�jǈzB��I�<K0>���$���+����n,���93�B:i:��Yo���OUe�����;Z�� �ϲ�"C;N�b򶯧ᩧ�[eF-��xk��d�i��s��6��v:��W�̰��0�A2�"��M�q���k7d&��+��J�rq :)�w %�B\vs"��s'�J��s���x�����c3��=� �4�g����WW���, iqM���A�E{$�)��ү���	������pm  "��oߕ�8�θښ�p8��^Z��pU�滺u��Lݷ�t Tlq�@��%�M�x���0[f,̿�ˏ���R�k���Q'��b)N�o9�<9:sX,|=�Y�
p��阎�̨|S��2BZ�Y�95K�:lhaR��P^Y��2;d�
e�����P���q��G�,�zvOJRM���>���E�Ԗn$��|c��}B�JH�:�o��鮬g�{x6h/VB��4h%��g|�U�����ݾ�I�4�E����[��?N�PȒܘ�A��v��tA����HdmN�g�WƔ��i�	�!��$�yc7�?��e�켔��j�kQ�󲇛�SI��Q.��>�p_����}��M��Zf��rT�yJ��� oY�#R����԰=�'�p�%k�<%�+������Lw��Y��o�G*x݂}(�.�����_=�B2H�e�ǝxqu�F*N�ܗy��`�)S�D�T����`�1�@�� ��7��}�5{�@	�i��Áy���Y����x�f,��v֩7g.��)TУ���`{�bK�\���+�TxW�&��1�ś�n��;K�"J���C���'ݵz�� @>®�+�D૓7$[�j�8ÞY��PO��Yw�]8��AQ�Л3���]���H+�����9�7Q�X�P�v�B�L1�Cm�9�-<t(����������2���=^�xb�
�������kd�#/ůs�t�)
��(�=�4����Ba�T��4�^v�i%1S�@ ]nv�2b(�ޏ�ޑ6�Q�IL�㖼x�v���%�'���'��/K*
?\���
Pà4���%���` @���v_^���:_�����n�a~e�s�J�g�A}�?ԓ�Ur.�D��y�!��i�X��J���zOk���p��Ü'�'�����XYR��f��2�Vw�GhM�����g���t-
k�Пg��}��Lҹ����e����:Z��>�{�YY����"7ei�l�jbP�D��O)yw�e�9�yߣ����mv,I�1��DB�Q����tR��2��◉c,�UQ�	����-bin(5Ŀ��R����dF�1'NW�������;M�??,�>�z-�o2�,�&�GH�a޸��89�}&���&�T�QN�<E�x:����.dh�U�2w_��"�2z�J��`%h�����@I�$1�fq�ii�%�cX5��pIť�o�$V�rh�ĒV��x{�}l߲��`�W'�p�#eQw);��s������mCӜ2,0 �ћ��V���4�2�]ꂵ����*!�ꕜ�E���5���gE��]�	\w���� �7�xk�f���!��7}ww����?B��V��a��+��9S���1�'����O�Պ�]��6�d�~�c�GCvJ��KZ�k���&�U�Zl[��b���;[�nY��t�V1Y�����ZT@io���4�$c���C'�����I��!>���~^u�0�#K첡�G��Ӝ� gE8*d��{y�RQv" �E�����Y�����u/����[��F��ϬV�%`�Yr٢�`�����<�V�_�%�7��m{x�4df�����e��΀��I��>���!��F���ӑw���^=12���T����uH;�>�_$	_�R�;����֝�46��&��h%U�Y�/��~�F�1��Js�8�ݍ�pK��U�az��#1m-݀�p�!���j7iu�\��I�:�$���Ȁ�R���Ο#��`
'�B�}���UB.�ĩnV+俌J�4n������ioj�^�\?��ӹ1���2{��b4�ƃ�(-�,�����0������vv|�$��D�M��v�}�g�	u-j���k��:��n�|r-!�s����g���P��%�����hʨ�CP��F�H��<�h9<�g��eN�aiL���Y�k�w*��E��10�H�3���U��W�C���Qr�"a����谉r��ɡ��>1x��WY�R���`|C�*�H���=0G�[e��#3�1��1(��Ӽ�,ֶ�=ݻ���i��6$'���N�{U�N��^�?�a��L����L}8K�~�����ak��9	]��&E@/�2Nw���J�����ۡ.�s��F�5M*mK(�<M\��%�Ů2���u��U>+�[(�03���cƷ�@o]�p0<+�^���i�ϙ%�1��a��Wz�e��6�H�x�׻Tɓd����z���}z�&�-�yk.b����,�E�'���5���V�B���%�~MD�q�W�˙*fQ�-�-,V�>��1��)&��p��yn��x�O#L
�;����畦"��k��x��uBM�������^��Y�l�w�/��K�Pkd Y��"�Sm�Ha �G���р;���1�=�'B�'8���������<���8��u�����v�|>��h�@F	Kra��}�*m��n�bYu�H���ڨ�7=�
~�<L�I�/̸l�l���7�ꮥ-�Y��'˖,T�j��A/4�<�?�OgrJ%�X��ju�m�cG�4�*1/� |Z��4�(��[#�cv�e�e���ӏQn�4�]V3n19��>�d灀0A�l���p�faŀ�+�q���J&�Z]��Q8�~������A�����r6�1������JL����S쾨L�ܯ�y�^�����m-����%Ah�1����9�#li$�U���.ɜ�4"�/�CT��*5�$�����m�Z�6��O��=R5�t��9`-%m�G7��Aj�Ԑ�w����U)��v[�b�}?q+���IW\`����	t��}u�E�~cŻ�����yVc b�4�$�2���Z�GkNm���#���C�Mq���ƣ��E��~=G��vN1jga��*0Sn�n��P�q��\[�a��9�U�Cn�qb"�0�L �|9����\��3�ă�<e0ֹl�o�{̛P�K�e�H>��Jx����N΃5��>�Ԕ~j�����%_2v�U���E,O&��CB ��L��<� �F "ex�KO)&�O�����^�=�P[՞]�V%%�P�s:��*�i�st4��j�6����n�מ�O�q��l���0�fã)�<��3���nv��U��{�_�bC��:JM�"��l.���8&l��@H�u����R����n�!M���7хpξH�1�6��nw�S֤�5��$�0u:�Eȴ�n\=: ���5���������4���E�B�5#�s�����ީ���Z���J�)��� 줕�R�N���i���&��P�.��6�[�X��T�r�lDṮu"�v�QԕFX�S�h�}�jh���7�uC�h��ˇBf"~6O��22ɗ�dǯ��=���^����n�\~��EJa�ze7�������Z��:p?�����ښ�%��ߖ�Q��^:d��(���K?bK�y�)!��T6w� ��]�I��Ĺ,��Z����&�������1	��� �w�?�^O� �+�+�����Zm�-MR\��cE��	��>0Q��\�������W��6���?�K���n�Ӹ"�f�����/�^r&�UD��bXt�ysR�w(��Ӿq�C���w��'�7��l��� �鼅��|���X�����lZ[IIF0h
��z@+��0�"���F� z��\��G����_N�����+���������ħ�>!?)���)A�~3(�i��1vS���O��?�Jtn���`��s쌓9��/��%k=��2��hџ�< ��hf\��(j,h�Gَ��?� a�kf�{�.b{�b�b��a�1
���c��*a������ϪoġŻڥ[���uI=\�m�H�/	��m]�?8�7X��Ę8 Y���G[�	��v�5��UQm�����䱚�R���)Ņ���N�����U�*��b.�Қq୊�.�F
y�X��-D��OY�<��`~�u|?ϟ4��� �-�� �W�����lF=�ZDe�}9J���'1���p�Lx ���rӱ���-[�^�@S�I{��8&\�/_�^��V����:!ŷ���ڕ ��J�������n�!rDP��iU�X<�orBL�B��q@��sC�2K��b����$�=��A&pnL�q�};�=!e�y����"�nLн�`�掋��|�z�M-�M\���4��K��f�O�gQ��]r�Xql��I��#�����^�&� ���� O}z�����-e��W}�>�廥�n[A-��s,�����<��d��Q����L��vʙ��x��ڔ4�Ǣ%̰��� ���x����s�u�[g�R}N���8�F�I.XTkT�s��Z�7*�aVd�R^Қ^���3^���TL�"ݍϚ��-Ћ<��a�%��Id�μ��31O�h�5ѡy? p��HA3�%9����w�<�˼A�y$���܏E�0�o/�Qpp?t������8Q�A��ܥ��d�����&��e`J�/T��i�b�n��F|M4���2*қ
���4Ds;����#�f�A�<��w�|v5�m`��S��_�Y�~����Oo�{����Ҙ��H�?���4�5}�6<L#��	)&�L�{?3��m���a��;�w��B������5C�*N�������[�˵��.�^���:�s�=w!��l� :���
�t>	����f%B�B4�(픛!�&6{Jr�i"�f��K �?������H����dZ%�[�G󠑶ѽ�06�Q�"�[�>�o[�ڲ�nU�0y�I�Z�
/��<�,�ަFv��za��12��O͐�h�J�	-�G�)R�����R}U��8�,\n��&ӭ&X��ڙ�UBB��Ч�/��Z��n1�����ܨ?��p����˕�nCevbgv��l4G,�V� ��u��%HbF�����wA�R)�D��鸟nk����ӈ{�r�d����s�g�G�3�w��^GB�Vy��)�v"�,\˘�Hn���'D�����`u53�By!O��i���9�]�F����ۈk7\o�:lq�7�?�"׸]�E�K7��uFyQ(K���e��4�9�[m!��*�!SDp�e���u/aKZ�LJ�<����ɮ�z��yK�-�b{�h�^����bt�V��%viMw6���-9�Y�1��[���.�a��&sK(�L�n������:oyK��$'��41H�V�>�>1i����
u���(=�{�����n�ޟ/i��2de��1�AL��,�3���G6�~�[��)��ޒؑ�f��jm�S��!S�;��9a�>�K�4#���Aͼb�3�F�e�1���}�d�����7�VD����_���"�w��v�H�0� ��D7�h;K�����`u.]�Y�UB�&V��ˮ}���ỳ^2�N����K�%#�R�blCŠQ����Ө�p�ĤA
ײ@s:	>�b��lM���������M3�l�r���:�����B�-A�艣����q���"�B"맽#�נ���4b�Z�7�?���@�ɤ+dew��h�O�1EJ��0C5"{��U�+N��C��[E��;��=�1K���"����0�!�d�&�0��u����K?@'(�/�?�R��Z���� �Oio��)�rɡ�%����v�\Xha�w��|�������;ds/YygIdCT��&��8��2jG\�i��6<#k��  A�i�+5p��ښZ�\��]� �m�˂���{��6��a|`� @F�JRb�1�kd�!B������)?��$�+�S��c����1�  ���/��C��ls��[lZQ�AW4.5^Ȗ�Q&�p��U�w�.�ۜ��Q��r�B{�p���[QĈ���iH	u�F͕E�a���b?�:��7&�0����KxCH�,�6�q�5��W#*�iE��c�v��m)f����EfG-�A��w�k��Z{����²*�F ����o��8������E����gз��|ﲎ�t�5Jxw�H�aN��)E�b7��܃���j`���[ʺ�lN,���ꦔ�M����I��K�%�δ�&���- ��C�)9w�f>��Y�۱�/D�����]l�g�����6şM ɗ>��:�eڅg�jF���"�jU�^n���\QVâ�V�b,��Zd�f��@R3�9�5�z5�V�X��j�9��ԹM-��$�R�=qa樥������Mvn4рU�k��+4/�:��˿�i�T�C��A��&Ƹ�!Ih�^�y	��������{qC��PKe�e^  �h  PK  �@�U               word/media/image3.png��eT\ͺ-�w'xp�q������n!�ww��.��Ӹ5�����g�sξw����G�Q�W��U�T�9���(/���� �$%)���������>Y{�&)Q!U���UXM3��?�����Ŕ7~u(����y)�&���zU[6̅�[���j5��Eiߖ�)�_Rn|��Ve�8���Z�P�]c�$���=������
Fy%���#�!y!|~%	?� UHf2p|}�����ii��A,cB"���e_�.q�����lG,ު�J�ʤ߾1O3999(!**IZ�1}&�M�|[��4�����t���*ڔ7�'I�ᕢJ�*.��ׯ�����R��%���!��u���k��ѧ�ق��(�ؘv���AXi��qOMa�p��V�d�y��{�b��3���Lr��(�N@ G�>��j�s��f7��\EXr2���a`H:��� i�de^�y8&��Pe��q:����t%V��`���ޤ^�3�v��X�F�W(�Vؔ��k�Q.�� X�o2�d���r9�?��M�K�N���CnV��+���3�*���ꅞ�z�~f�D�8����J����Q,ygw�B§�G�@�!y@��n:#��z���j������ѽ� ��w^�IF�R�������l��S� UJoM�J��b$���%�>P��Yà�����<�h��5ٗ���uՐ�� �qw�r�Z�6�����ϝ���X��*�����4����ީ���-�t��3��*���$��S�v���y��B�
��p�̭἞o�E�Gg����3�,���U�IV/�w��䙽�����AAAW��w�L}"D��f��l���?�}���v�nV3�_A��@W-<qέzMw�{}b���1�5[�5$��h7�
ȟ���nzo�VS�{�r3IW�f@ăt�tZ�}��'O�;��X<<\8��U��u>9�A7�����mS�^�S�K�d�e,��ԗ��WO�{�
�U+{���=�K־��{�*��q��ƷΝM��Z1���N�����?�Wm'��`��V2h�1�-��T�9�����>1�l�!/>_b��R�U����٥����[�Y��g]]�"�ƬiB9�R�ɱ����>]����$����մ�[�~�e�p��Je5YKo�[@&�	���� -�&�����ˀ�uė����b���ƞ܋��0�����Q���ɨ��laL1�����͈g4�D�g��>f�t0� Y�x�����:��uX���M����!��� 0y��7�M�[�|^�0�h�mr�	5ת_@9��7�8��*N|��4���^��E�U�>��L}"�����A��\�VE~O�����a�`�[L�CUs?�ec��0���xi�(����7�@�s�țK
�&=r��La�ˉR�%�D�ځ���X.w	_Z3K$"):7���F�	��5�k��P�'����5w������t���T�0�(��+=I�D[�Ù�f����z8O���Dl�K���T�S�7u�� %_%^����g���i�����;0#?\�()�x��PK���DB�h�8��},�X���KC�w>M}�؏7<:�;�@\��;L�,�� ��ׯ��k{�`UP5��ڸ�? �#��x>mo���ᡪ�ǿ��Z�!�ʍL֍[n={����"�Tc2E6G�9�3Yo<�3שB��p}M�	�q��3�� �}�]Mc��f�k���`q!�Θ�x)%���';��W��/��U��X���������|wI�Nxh��6��%�9I*���E>9��h l�R�b,�B����xL��y@_�o`8��*��zJ�&m�����":	��<��@�]A*�k�\ꖙk�i�R��?�ռT3�����[�5o+G�bG�0n��T����.��c��e����4�>F�c�^g]�2WUv��OXH�YISM,��!�t>9�Kn�.z�J��1&͗b�%1ʓ�� �D���D.b� P��H5���J̙�����G�����J�Ȟ1w�`���(f[iA��Iȇ�A�E���U���,l2H�{�˿+�x�Pf)��FS3no��;��o_��a:��i�/�I���h��?��$.�mrh夒2^O�$�С���L���֊���e�^�J��~׃���>-�=��R�v�qs�����=�.�#BF��t2�ٔ�aF�a`���҅2���0�)�k'-��m�VK�({Т஑���hg�u&�q���K�H�g������u=��>ڤ^Ʀ&�/��c���3��w�h�$��N.�j��r��e.��:R��p��S���\�we$���IK����{�f��I�	D�Z�ۯ?�Hk�[���
�,�����}qi!���;�k���52���S&dcJ�^�# ��T3�f��j�K��읉gT����ʣ�;lB����t
6У�?;�#7>��]K-��A�4�����%��#z�!���x�5%B�1힘��H6��9Wg;�ps>�0Ү��T���>"����ݐ�h��p���t�����	����K���F)�ż=���W����Sz����uW2�>��3U�u��G�B&���J��{/��圊mkUL�g��V�N��.O*��b��?�H�^ޙ�H���7;��/�L���kFKz�Y`��tap�':KS~�)�ˉ5��?5oP�.���1�
i4zу���W�+��yo�9�.�_��?����M�OMoV����F`}��r3	Y�$f4�Z��|�M:��='��ޝ��K
!4�� P��H|X�]اdj 'QK"���m��2�t�&_n-�+/���%7	�V1'�������yM�� w�n�����M�%"�8�|��`����h��S�5_��}�V����]��J���\I�w}U��@\5@O��[�B�|��;k��/���?fbU	Va�6�!�D�1�F�C|fRS�_�@J��7Ӊ��`�@��l�R�נ-�R�'+�:��:�� �H���!"�����������k*��^�C'����kf���:����% O�}���䙹��\ ���u��f����%�۩x�j�oc���:WW<S�%(�ƈ���Mߊ$j��lym�{�T��}���Z��X�|�!���Xm6���)�v��<+t�M��Aנ1�J�J�Q����̧ڧ�$$�hG�y&]�;@�xt�/Y�Q���@��D�Ч�ȃ��1u�:he�-0q$��������9'����:��wF�vE��/�ƳV�k}��������f�[��s1�|b����t*sݺ�rVʳ˄楒�O��XV=�{E^�F2���ѱH� �mɦ��8və�������c9�*�8&MM_�mN��K�x�eC�2͂��˵�-��/'�������x�ϕ4fo�]6�[8�~s�ђ�TL�q�L!�
�g{�`���l
߱u�&��c��6� ��f��Փ��������1"��;�$X���:�ɨjy Q(>������Cm��%��{������eOr[;��ܑ섶�g���C9џ��u��� >�<�7/t[��SڳVC=v�jL	��U���˥Y����*�V3�|m�Δ���yl��ż|�A���H�SO/g�{��aޯD�T5����m���E�����~ x�ܐѪ	#�C���ݎ}��ɗ�������H���e�cg�o.#�K��P�l�n��톴�)Jw����n�=jLU��u���\>�6T{���8�4�(�&�!��$�`/p�)k�[���N�U�����;�/�Gy�ܞs5� R�,�9�����%Ќt��C���� ���em,���D\-��Q�e5]�4#B��y���dW����gr>ԯ����ni*_�QC�i���/���5("�G�i@��s���ڋ0k=�s��F�s���0����%4cW �����-�x1f�~��|����q,p���o�/@�Q)������6܇jk�-rM�J^	1a�j��q�p-�*iVŸi�2;�޴���Zk���#@��e���?
��r�XR�x�����Q�]'�IC�mx:nӳ ��d�z�>w��`��R�]��/H���yF��/a�����ɱk�ڷf�2E�ֽ�d:f�K��8񕋠�w%w8!Yi��%=���ō��@H`>��8_>`��a@Pi��'5es:l`=U�������}����h��߳�.GM��i��P޸�\��e�<O�蜭u!r��%1�����Hh��i��JG�вC�M
E�9�ĭ_�F�7BVPԿ&P1�՚t�b��瓅�xE��I�b�[k�z\�?X
�]���ُ����	hU���Uۃ��7�U*XM)J�̗r�d��J�`���OA��1�]��~��a�n+���J���5z�m!I��[�3j�ı����3z��PQ�0��%>�k���O,�NQ��9{p���5Y.����[��6U��w`.sQ�s���)�uw���˸ɫ�rQ�Tq��	%(�����A�����L+̬ཎ��y��������U�]��0!AqhBz�KC�QB�6���	�UP�b_�{���fD9`�8�
��ŴS]+Rl$!�r�G�%�02ڣ�qm���Eel/;P���f��H��m��f4��l�qi"�3�>��88��X`]�W6�ɘ�����N|B���N����
�ZUY���qK�x���VTMB�L�ט�χG��qg�kp��_fFkdD�,}MB]�T�ޓ}m�8&���_���3���\[���v�m�rgk���9bs�~^X�XT.錹A[���vZ����Q��W�kp ��P�1>�,�5����ID��\}�6�x���΋ د��9����>I�)ھ>~�_��q��Z�-jF��J�P��t�b;��[͇��l���	��������h���*r�U7���g�Վ�x��	�G�>�@Ig�D@S��*��(}K���=�l+*�����l��$�$���h5���ф��W�k���,���������-䫸tb������}�_���v�P��G��N�Bnz���x��W"P����5�q��蓦��T����I�A`
����"�(�O��$u����� :@�Ʈ�@Ȭ��M.@�\��O�ͩ��q	ȅR�b�5<��;�ӕ��$)btj�)�)�� ���2��Rи8�CM~\��(���l�SQ��ׯ_�m���<��?�����g�	��˞�w�%���ن'VIHㄠޝs�-MygRF%eo&����zr%0�Mn�W�H���>x�j��ݣsA_ׯ�v�&�G��|E�Ş�oxVwD���P��/)9Y�sa2҉oGD��ϋ;��~n[��|Ѱe�(}vC��IIƀ��]c;�=K$�� �+�M�06���ꋊ<8	���M���J�.�^�h=�6��v3��d,�õT��Df�ڷ2�!����z(:zY����珎����:���٢yP�U�|nc�;L��Ӵ��{�Z&�n�%��Y+w'��fw
zx�󏊇t��*�ٻ�\�X/!]Œ��jQ2�G�]��І�R�T�B���:�����P�0_�T�����73�g�u���=v}�ˤY���F��{�{S�G�%C�M)Z�}l��,�x��%U�H~b�z�����"��r���X;�"Ǿ�sZfi:�/Dj�����5�}8+m<�_��)&;����U���:~~��Vc3�m\����)���cLd�4I����W�e�����������~�U�E�j�X�~�vDҞi}�G�}.���D*�"�)ަ��W�̬�/�^�-a��2JK�Ɲ�Z���5enlv�����bq|��fo.����bd�>�����ij��윥���-�52�|���^�D��Do���Z���k͵�EM)D]�D����i��i��9�I������sO����rS/�����Pad	���~,�ҭj�y�c������)��ݎ��1Ґ)&y��2��d&0��' R08���A������KN���
�V����8�Er���(s�6a0k�T��v3��-�Ξ�L�{!����'�U��>�6|�b>����)s���iRi8z����w����x��:P�ɼI�F�g�}5�uы;��)J�TiU���g{��i�<�Ed�Ն)h�.w2�tV�v�Yx�w�&��yz�z'xJ�k~���`���F�^j�f���TW;Xo�(F%k��bj=3'z7}��"н%��~���E�h{��Tw(�b�)�K~�~fL1��O��T�Hӭ��w�8��DO��}�/�ké��B��c�6���h�����ة*�[�lr�&����t�J ջ�~�f�oIIo�|��U�Y���ɚM�˔_�E<���>v����c����~9��naկ�_Do�Z��$9�D�������tV�=G���e��)�-A��R\V9�g������~,�k,�V��I|B�-�w���ӷ�������l/lZ���ԍj��o	�r�K|*��|;;�Y���Z�����Wg�}����^W��X~���R�
q\rŔ>q:��'�4G_hQ==huoвz�X.3&��'��8v"�u�����U��Oqr�C]-bK��,4���E��^��m��l��,�.'k�^�P�@����=����,2:_ݎ��w���TZֺ����&4�r�&�3��nR���Θ�Ѩ`����}x����ɗ�;����� >����B��Q��J��{����/z��/6��H<��������w�\{�,n�͒]nnk�z2vV��W�V����r!����Ux���'�/T!�Z�8�Ā!u��i~�pjf�`��3�`PD+��ӿʷqY_q����so�0	ӄ�pט�ylm�
_.�+g{�O��Uc�5w,�<����D�M���D�ψ��l�U!i��G+�4�����O/0�a/�/�dKC�)�-�z�J[�6���ν�>r�Z�F�.�	o�����?K����??�?TY��U��wDX@mni��9���]�"�ڜ��w���޺-Z�Ln��Y�����J�1�hv��^�2�e���[�R�GR_<,SiWǲ��B&��.�᠄ˁ����e�	aۮ�{��7���˗���E�/��8`�v��|��O#���ky˧|'6�qcf@/O�|:���Gy�f�'&����\�N��ަ�`-M3�:{u�n�X$�ȋCL�-�ÿ1��YU�A��B��t�)Rh2HW����[��2%����͚k��H�:�8��o��)�U�`!Y�<����3�f:w��4�6�*Q��c�KKڸa����@�e眰�|3��'ɈX��@F���Ba��]�^�^#0r��JL�2�w��u������h���1��o#
f2}	�����������L���
�$�OE��JV\��/9T�%L!*��.�	�󻏷���L��R����!��/��{c�-mE�
f�R) ����K�/��ߪ�*�233��i
�/��)�*�a��E�E�	�'t�����?�6⽣��͈Z�QSY7^�E��k	
0;;������P��tv:��>���\g�K7��ಙ���En_xr �P����	y��S�8�:���[J;9���H�i!q�௏��f���MU�h���}k�N�A�) T���poՍ�չ`��ֿ͊XXv��vTK[*޹H���*��O���&k;������}���a�mF�i�p�w\����v�4��a�ߡ}��u'��E����<YІ�"9U���b���2|rzs�ݮRY��
�Q������|6��'Xs�H�_ڰ����|��1A�"�/�`T%��Z;x97��Bg~Z׏��II7�ܩ\	s`�U��j��[��9�z�"�]������g��\�uvFKaQ������ ���7,f���ɧ��M��> ��.����mf"��-�흜N�{����m�����3��ݡs:���Ŷ(?�$:�{�NeJxhVa6�<_#}-6p�!.�=3�}��ݷ��|�Y�v3�15�����?R�� ��vÜoƄ5:v�@���)c�k?���:��2��ÿ��b�g��9i����jjX��^����r'�0�y=�����Åǖ�J���]]S�H�>�[Vd?�K��M�|� S��]$%�hPv40���Q`+��U���Y?�G�ܙt���y�b�ܷ`���+W��OR����+��ĩ��|�=����g韧ەH�@����^�I�r��	d� '&V�{�~5eM��}r�v�bd���.#Ni�H&�_����gv��U97��r�����vrʦ�>�LC�ڒ�Ł'�t����$�}��	2ƍ�K���	�;��m�e�T���Ο:vu��*o@�ww&`�����ϐ��I��������{�<ɹݘ`QH�.�ҹ�Y��tw�*�<F�@�o���v<���~�aw�ITN��/9T�Dz�/a�J�<�ki�����)=#4���G@p3�n�]6j�-�l���A��d���\Ant���#�d �.�OP�W�xӊA�4����r˓}鞐�2͵6\�j��r|��c7�C_��srH�a���P�dQ"|�"�"��X��"\�2���'��O�P$'�z
=,+���&��Vўn���S�w���f:9�l�l7�<q�q�4mǼS�t[u��|�S���9'������D0�ef$�Z$YWR�ȉ�PN�x�-J�>Y���>@�U��H)��!E={�f�<��h�EE�߆�1U��� �^��Ǭ�������Ip��;dV�,m3�ˉ�[�ӥ��ر($]�3N&�����_ %D̵h,�4��F7��1]ꀌGJq}3Ll�-}g�]�VX���<Фw���1��Tw>_��.�I���PZ���r:ws�A=&���[h���q�%��0�gÏ�H�,G�Q�� �,M����gh��~�Ysm̺���c�:"��0g�a)W#�F�6�mO�@����+�P�_�䂬�!XeX��q::M�х�j���-��ڏW�F�$&PZ@/���[SW�mL�N��dͅ
ڎ,���3�.�8�V֞��I�OZ��z����%r��c ^ߋ.��;q��-�B���!F7�م4�h�5��h"��n�߅�r�/&�L���:ӌ���R?r T�䯁m����8��F�"Uq޼�����dj͉�ϸ{:AM���?2����Ѓ|T�^Q?d7�����n����Uz,	�7�{�����q|,�jz������"��M�Є�S���6�Ɨ�v~Df��b��d7�A���!���pWλ�~{�߇�8!� Rߜ���[�-Ҙp�L�6Y�5��~�p�%`�D���풡`�<�'��3e��5Z�����g��/uk��CK��JP�|�������	y�Gd��ˤ�	yQՎ%O���j���6,A[,�i��n�&��Püa��o���y*]wB	3�H�/ph�|:|�� ��ގ��Ka|j��)���fhA������¡�rp�����X�]���V0�e��銦�CCC?��e�0�{��zO�K5�\m[� -ך��������pV(��=w$@<�t3qq���|�&�֮|�񑔶/��A6������.�4JU/7~�+����h�3`у�|y~�;������6��Q�R��f�X?~�E"g�ؽ��U��3p[��A;T�w���m½�݁�a���*��I�
�A��TD�'��lzGi�x�^/�c��y`�:_���P��+����QoI>,%���\�7}~�	��t��W[0O$�e�
��'S�(�u�<!�F�x�\3ϯ��v��*�K�g�#��Ԩ�r3M�G/�������.E�=��Ulw����^wq��4q�&�L4 �mM�=���wj�E���yeC�����uq=����q
�b�uVAK��+��J�bd!��I�B,����[�w-����~����y�
�VQmB�إ�4��ǻ�ȗ�����xILR��n`�k���wC0��Vq������q�Bᄯ��TU|m�����ƶ\�=���N�$��d����CKۏ���, �����i���K���S��ԅ�)c��QR����[�) ?c�*&��Ͱ\l'B�գr|5-��1ŝ�w�ovxF)02�+z�����x{X�TE�s�dVF���dG�E�����>������-�c��Tu�)k�w/�
#qk�@k:��rM��o�!{�O���J�Tho;��+�p�����BM"�#ʑg�m�uπ��v�o�U���:p]�C����ߋ��E覍Q~MU��]��2H�h��G�����f�V���'k)]kf�e� C��M������/J���\0�)U���x�r��:��c���ھki�-����k����.��=��4z���m��A����q�9�iNĀ4�kϪ=��'g����0W���s�������x���~e�i<�9��ΐ���6k��������Z�Z>t��!d������tȗ���Ҙ���Z 1�k?� �.�?��/Ѽ�W��1M`)u
4r��4���5Lb�ub3:���v�J��p��Fn���d���:RU}~�L���U1`��ވٸ�J�����g�#Ϟ� T�����=3(yp����K���F�\�ʢ`uGq�\�6Ѧ'�;���+�~�h��3rڣνI[8� b�>�j�Y���ٻ-p]���o����]kn��1>G��6��[wn���tnE"���nv;,4��sYE�����Wy��+�ٌ����S�h]��j%�@u'+-���f��l��l<lC����4b��,��5�ZQP(5�/.QݮQ,G��g��B#H�%���ďݳ
��@�����Pc��'�	K0�f��u�� �ي^��� ĝvxD9��E�]���
� � >Օ��pz�OfvT>!D�6�����'$!c��)Mm�Nt���t���������$g>!����zAF��O�$��k�%ɉM�0$��S�w��{��敖�p1�ĥ�`�����u�Nm-˙S4Гe��������Z��OB�����--��X�;���Xo
����ckPoj��M(~G�Y�V�� �k�RRs1�;��n�VG���Ƀ�qh�Wq��;8����6@��4��F���uV�Ϋ��s��8���*4���U�I6?\ІZ�]�Y��K�6��������-�����~���cu���f�Bb���9AR�c�ǉ�J�b1��^��o���u4&��fl��������F�d�}�z♰)�x�����"�.��ͪ�H�X�wN����"W�T���f3��W�vcc.�)~T8!-~�Ti�]l9g��~A_m���6�[zu�脭$�IP,�_
��l2�'�)��I�g�r����cDҏGf��������t��j�8�s�7߈f~k�u�}ӷMūXU���I;��a"?�t�]�n]�����=f�ZΧع2����4Q?V	���d�#��Ҟ8�x���f;�!�yHb�H��G,��/���M����;m����Ir��bs��I���)������\��i0м���$F8������hM�0����I�w�o��@���j~W�oz�k���Ö�K.��ue���q����C�s>�U�廰
8�@�{������9F,B��u�=�)6���A �Vn�$�FS��	�
<�,ez~);�g��~��J�$Ɇ��C��%I�?�����M�jx
��8��#�#.$�Yl���ͫ��,���&���tQ�m��~#--�
.�{�s�����޲o�f���ZR�3��ߋG�~%�i��2��y\�8�����#����3> �rm�cg�Rg4���&�zP�Yc>�4���~e�������������b��V%�gT���LD�v���3���-�
���F#������^�w9��a��W�G�g<	���n%l��,�������P2�uc�OR�p���]��7�O���EVƅ�ɤ�uX��!���]���+F6�?����9�;G)7�����Q'm?f52qw9b��u���>Т�f�
�D���(�����`�˅#a��L`1�|�,�E�V��?���A�$4�62+�K9�B�Sy�%Pev��C���@D'�٠�.��7V�v+���$D�m�V���{*y��y ��}?��y�����)=�L9�C�V�ZjR�=��תq�}��.��$��PY�\Rzv��f��y:�D�j��������o��m�W�~���b�c�A����K�6�Y�g�N�hc9�>}�I(y��'I�
�@�ݼ�K�9�W�k#jS@�Іzp�`��1�n鵺ۋ��j*6����
[RFg�|oжg�U#�G��u�u�o�j��@�y�y�O��qHų���*��Q%�퐸����޸��f$�>=����`:y*�<��n�}p��t)2��͘y;�fA|j":������L�����K�&&�������:��S���A\m]��%�r��Lb
D=��@��t�T0���̈��W���6������|��!���?;����E�m�	�JԾeƿ�j~y�C��E=9u\i`���X ��Q.!����9��?����i]�w�Z��ȨD��m��Yp�h+0"��]47ŕip�����d�1@�0el���W���n��T$U٦#�����"�$�����,�hڞ�T����K�o�n=��5�L#�-��v"�o���z`~C2�M��J�J������u�q��淦�������j����f���hc
b�5\v@���~:��L�X�jo���[�����ҍ������Oס�H6�K����(CT^cwP��Z=:9�0�E�n1�	#/��'�R}i�	x:Xfm��J;��c'f�2�W�I����h��y'�
,���'�����LyP7���z�٤���R ��v�" �H��l?�B.��a!�`2���q�<�yAZ��^ޙ-��uB�BȃcW~�1�A�N�$���ݥƱ@�3��~H��|6;�T��w�-�8&���5���W7|��H�5.V,�F�y��]O���/���]Q3�]ş^�s�D.z�_=Pu�2l�"~�^@��_����i1��GDޗ�.����������x�	J����fL��D�9��ˎ8��b�#��g����,�Q�;ŷ����bP1��+3��h�|<�o;��$S��Xc�1
g��of�:ѯ������,G�х�X�q�&��.��j�A�6_?1%~0�{ڻ��߭Ϳ㌏܈��V�ll�Qay0B8��
� fu��I|5�ρ��Oj^G�7\#�Y�ʍ�:��?�N���HxϢ���_��t�����)��(���7�#������p����](t�V<<"b�m;�F���R��?� ����?�ك� ~'O�g�c�ZA�}ګ�:�^D�JޟNH!ﰦ��I⻱r#��&��?̶��4��ۚ�w���C_���&Z\�=�{����{���Hh�(oG�>��B-u�'h�Ы��YAl_T��^����}[�ϐ׳j�Vr��?8M�H&�����rs��������B¡���,��)4��������P���I0�j:�˧��X-_T50�m��k�̟����>� |Rde]����]v�N���u�0���8_��WkHg@L��>���ؾ[��Ӌvm�c��i.P��2�D���נCM�*0���]�&=���I]噡�������N�Gf4m���Y����y�����U�ɜ�e~�h�����xK�1����o��UR�\wC[b�.G��?*26�?��aIkB�g�
??Ȫ�|�-&8�h(��N�W|r!�B܋C!Y��_Ylm�jAfC�����s!s���ŴB�0����L�BS۵��Ŵ�*�k�Kd%ۦ����9����刚r'����D^۽�e<�d?��T]'dתF�dt~$�'3�r.��{S��ȂB���O��{>�#�|t}P+ގŗ��'V��Лʎ��1��ƒ#�hW4+���&��������&ojp���t���.y1]K���6��s&v�nf�Ln�������!�]��c}���1����f�����V������s	g[!fA�썉S��[>��Z��w��ُ���IjUJD���ŷ��.���R�����B� ���by����&>g'K֔��2��BC޲{�/C��q�¡�����M�\Jv�7���ǚk� 6�GSO��ҩ��l����Q϶��s��@����eg�����-��)�\1�����Q�d/.a�9�'+/�3��b�ze+�C��d'���;�<�(�i�
O�`��+2"�Z�Ŵ�dK&�\����;��]�o�@�~V����;,�;L�9��zv-%s��|���ɮ�8�O<w3w�Я%Uz1�E�� v�d�WN勤K>�����~��|�%�M�3�M۬}�5��q"c6�Ewm�@:&]#b0$������ܝ��'W��-�������a�yݵ�$=�U+&��֠�
.S"��,��ޱmNѴ�I�j�*�Ghi��a%\f��S���d�f�~�[��?�=(�Ϯ��fHF�ʚ�M�@O�^����5[�3�/�_�p�T/F���p�R��.7��9�Sw3>L�yB���|��7���8-f�ˁ�W���6�zL-�?��ѽ[[fd�=����2�)���t�O=�]x����m��W��Re�����V:`��U5|}&��I1>D+��p1��.��d�a���X�7>�hu�z�]��0_)&�ˏs7>ii�r���&��U�ؗ���epDx�3o�V��(����}��f'n�|5"��G�"��&�y����K�ݵ�D��)��)%�}Lܾg�}�8�SZhzol#�����i�ۅ�s۬Σ��s�k����7�bz�Z��T_ݟ�)�a#��і���	�-��P��b�ÿo�:x�QG$gX��0���o.�����͠%f"|�A
+�qq��E�J��n�sdm<]����מ?2Z�RV�N�7j��9Bo%H�� {�'}ׅ�ɣ�h�NDE%���5�[�O��+OZT��G��/�h��G�B���m��O/F'L����O�T�A��4���d�۬�e
�ue��on'ݒ��x�b�WE5�s���j�� �q��ٺ�x@��_��fw�u~t��������ml5	<������u�Ө�?�BRoA>;vחO���-�|� y�X_P�qb���JV_���Q\�z_�vo���)3��B⯶��E>� `���]�����KA)�ǿ-�X�N��j��xTR�q�����6�%�$����	( ?�I;����-z�)Aa����褲,��#q��a̧ ��!�����(��#�߿N�ru�w������iA,#�j4Yh�@YOV�E;�#���I�fͻ���e�*=�E0�?4Z~踑1Wf��Oz�ɖN=�uʣ�+�D"2L���Z�Hle�E��L�F���"5�6{��@':���l}�����u�F������!��������&$�CR��]9��Mh��G��[�?!v�7z�	����K��S�F�g=Ԗr�@w�]ii�w�Mꉻ��ňW/�����;;�$�T�}�r��@sg9������럳��ݘ��3�B��,�_WS��y��.m�����F	��iU}C��2�P�/�`��0xE@��m�ߡ�ۄS,.���m��I��%��lM�A���<*���M�-�lC���'Ȭ���ř}{��jՌ6&�׌);Z#w��4�{���|�#Xր�\�=	UqG>Xi�Dn
���$s��ŦQ�0�f����Wш���2Ӹ*6�_ 1S�@b�I�`6Ŋ_%T\]���0ggx��1 ��*�vp��D�؋`Vu�L��Fg���|���`yJ�K/(�������H�Fh��c�E$��>SM/���TC���`�R{��|0�� �91���	���i��>c��j5[�x�o�v�P&)�ho���׶D&�n����>}iu���ۍ}�N��$����@���2]˘������:\�M�[�"�Jw��?!����鄕�N�{rj<��UJ���]F���]0vl+pPjIL�dpU����0	�T���|�8�:"0'��h)����
^�{^l*B\�S:;��'=ӛ,SS��E(�i�͚B��H;ֿf%M�~����Q�\Uv���I���\�ÿ��Z(� kfJ�]����<	ud,�٠e�:�u�HE�* K�Kb��g�W#7˦�?���,��Ly��06��_��]#��3���^ E|�,!��izʺQiO��R�,1S����9Z��oХ����S0桕_�o�EWv��T3���J3��uw�����D)��ke7�yq���S�k�< Ww7�_?�&Ȭ���a�9���j�\�`�8���ߜ~�_hIi�p��I�k��ܠ��92{|O�[O��|�fͩ"VC/��۽&�Τ���YEŕ7�8.�=@pw���@�����@\�5�����N�����d�yg杜����W{�����wU=O�������CǞ�ԯc��G����YҼ�O�4rs嬍$!V��,��on���� }�~�,E�P]��Cg�I�c�Γ�E�Au4�A���4�0�P%�3]��aE^Oj˅���R��`����t�}�0����e*��P	������8��w�KW��/S�$��.�-"_���3�joq�<�ZJ�||7{d��(��c�ax*�EK���6��Թ�����'���w�5��.���}Z<f�����1��7�N����0ر	��NZ�m��"�����[��;��ɉ@�3��k|����^�qO"R0�#3�$��1��q���p��������_]�mf��
�S)d������#�;_����?�r���k�B��c���'=YF�K���G�^J������M$�(|(�x�V�kEN��w̤�c-��R�G�8��J�q�{t�w� ����.��3���`�6��Ȫ� �e2����Aj^s�Ժ���娅?t�`�{�o�w!s2(s��(1��$�LD
���&�V�5ȕ�6����՚6ջ}f7�r��t)V\A���%�d5e�4p�ĴU�Vl��͇v���������<W�8c��J��L��.�3�F��7�0n�����ᓹB��~��b�C7�b�uj��O��	Z$'NC���<A���jT��}���
}k�i�Nc��R9l��ﾭh�Y�h�n�v�rW	��l��n�o�W0�����k����9^+	���͇D��`�4k�͂��k��tß��j�'9�	E�<J[�|2ͭPJ~9�mcѩ��A/Q�G�άBh��XI�"%0��!_���1j?��W�'�&m�(������(ݖJ|1H�ı]49K�.���ޜ��e�K��St�M���&�ͫz㣨x�R>6bn���c�y���`l��L�ɷX5:%�SV�w�^\��X�z7���I&�>�f��:i��l�(��Ҝ=S	�b�!}+7[�����n$j�〇 ��ڦ�2�+<�ʗJ�5���-Pۿ8z|a:(��		]�]XȌm�oe�z���9r�u�lȡ�
�D�a�/Q?�
�ie���'�,Y�u I���d� :��6��f�r����`7;��"���C��P�D��{����'x����SɈsG��T<,D�z@����Q��N�s��O��*���xwe�?�Y�@�ry#hDs7ui�����@~�.��{�5�� ��X����ˁ�b��ʉ��E]���K�8G�l7i�4��Ԕ�t�=G�������R��nst��N:��2zhf����t����j�[��*Tyv�aIt���|*988�&���%��I�%{���/3V�W+��D�:���y��w�$e�@|P�!�'�n����i�����y�
�{n��պ��c�!^�6x�NN�/>}�(�Z)���C�M�G��c��d5n��N/��-+/���J�
=��q��;��S�=X�"gx��e�����r����.wwDw�7Փ��	�D��X��|-*���Ѱ+�������h>X<��S_�/���iF�����X<r�d���L�_��j�2�ܝ���l�)�=e��.wW��N�!6��9���4Wy�		��~�cE�$A��}M�(��0�,N��v�Y���C��F�o�D���}�� ���t���
�/3:�QU�C�]��-�G��V��/#]�M.�\,S�(7�
�QP��W�@�����-ׇ�(�o�^�o�����n���є��]dܫ�`0}�c.m�igv�Z쉏��{��+�����h����-3?��"EU�s�$��޸W�!&�e��u��}2Cd��zJ&�]!}��ٻ��fJe꼟9�TZ����C�[�����ym��ﯢ+w�H��)o7%E��&�\1�b �.�P�&�MF�Aaw�:�F��u~?���N�t��)�^t?�!ɰ��\����n���drш�.�Z����Og;����DK7G܏٧�����<"�$�Y���5:�r��w��yR��p��Q���2(F�!L8/�a]Ȧ��e����R��y�~X��?�۝��[wnt!0'���KvI�%�N������ݠ���ȸ$��#���Wc夃�%�)K�=q؜��C|K�G�1o%�r�L��X*O�H����$`hv��Ƃ��׊���λ�ͦ�>���df�ܵ-d�Yc[��8&P�/���H�����iq���K�)Q�h�Fw�^�%�P	5s�f�������ɝ��̅Ԁ9��}���FY�4���"U��*g�,��,����R�l����Re���g�W���*�X�u�Sb��ٚ�!:'�A����j(�P)�q~�w9�����]w2Yf��'����4��Ȇsm��p�d��gK��h-���;O]��o���S�+��bkl^�-��(�d�kP�J'�n�pl_̆n�ޣ��.W�'�n�����g���S�V��H�p�����9R���ic���/�[��ZC�����ki6л&+jHQ���q~_�qV$�W��`��<d���S���5�9�ٖ6����SyB�������&��49��ڣt�x��<��g:ïk��ɇ�/+o^[%^H<�6�����g�����0���L ���:c���dZ�:':!D΢wcOL�0���7�s���u�Bh���|�rť�p۽'6�R�[��\e�0c��g�#�w�}���w׀���9=����y$[l\ô�Rl�nNCOrk�\L�������7�S+7=Jl�z����C�W����P�I5%�<�ߺ�D�9�
��ܔH�����ZErS3��ˡ��͌�M���%�3`Ԡޙ��%.�u���P��@̬��}�4p��TT�����i)<-}�������#��!�x�F�kL����C�A�ǧ�%��{V��G#�w4%�Ol���MT pz(�(�$Q] V:�Ǜ�tQ��v S'YfX��I~���Y�x��Fa0�W�q9�hB��u�����>����j;��&>��O�ؖ%�iw����d�~��؁~c�������8A����SG�����]�(hΊ�,�Ox\(�����V��h��D������^NR�Vx�ž�'IkdI$\-j��"�g�Q�@��\R�U��H�1��f&�|'?��goZ*��P���1�kt_?@o������������������@#rk�������_��g��XɅB��s׆�"Ԉտ��>�ؐE���ӗA3���Br�u@�4ײ�5���%w}	�k��zn��М�kU��+��\J�d���D`�V�̱�;Ƙ�"oSޝ�;�
��ġ�Ϭ��ܑ��j��D�uh89+U3��>,F�
=l�2?L7����Su�+n�5*�����m�$֐���3K��f־]��w��B��c�yw�����BÐq�� j>���k	uN���;�J�奠��W���c�:	�ʪOw���5�?NW臿\N�u��wͶ%�V�u��A{�1���?��M��7׶*0{�N�k���g�^e� K��T����ٳ�$٭2bR�p��y ͍�ǰ����O*�;[���tAE:;�1
���h.����)��f���kﴟE_���K�ɝ�8���A�s��n��3��L~VϿ�Ѻ"5_��;z��J.�J���i}8��v1s:�F�s���¢��"C��R+������k�zo�^RVU��(x��f�JV�ƭݖ�����[��z_$�������`N���r&Hi]�ܦ��YK|���Y����h�K^�}�V}	�:�7*�3�2�U{"�n���ՙ��T��g�K�e�@X�rVO�fn>Ʋ՝d��1�!��a�Ƈd)7�}��P���o6gF�鸑��� �0`8#����$�#O
��
�kH`�Dv�����/�� '�i��(]V$��gI�����!'��2̻5;�H��@����*�䖳�,'��FD4?/�u}��r�Ҽ�v�E��~�8ct�*�mɳ��� ����Z��>r�Mc>���݀�T����<9�B+��,�g�z������A��9v�w"v�7���r������� ��Ad`�$M���>?.5��Z!�|���Vd�9����׊W~JC���i}B�<8��c�(��ļ����(Kr�W��:�f�X��b��fp��`��Ӓ�sՐ�}�Nx��e�o^�\>W�N��TMp)[�7�����4�:eg�E�� -*��bf�JM����8Y���}˭ b���׹�rIq���F�A;�W��8$����6-u~+ �9����L���,ͿC" �&#}25����W;G )�g6���,�4�Ȼ��x�����9c�-S(�x��L5xl��OQ����,Y�#D���k�O����{�?��g3��r455�>#�kH~������iu��6������/?=OSȔ��" ���%轹��v���k 1ͺ�Z0��v�� FYX�%�G��ֶʎV�*y�S(\��;�Xn�W�Ivq8_��sA�`���
�Fi^W�U�r��
Hb�o-�C���ֵ�2�£ɽ��$�a�-\�́�%V�؛/GP[d�_�D��	�y�N��{U�r�����	e%�pU���q-�ϗ��S�f��K�	�S�*꨽�X� UI������P�8��<��.�;��^�x��E�zOv^Y��>�Y� jp���bO��a�xwU�L���ci�� �G,a�c�Q`�Y���1��W�UV���m��!���r`6d7YD���4/����EX�G\�@����(��R)�+���m�.���AN���w?�Qb~~2����&� 3�Ë-�
��$�k*J��.HOfz�v�����P�3�0�z�e �����-6�f�yu��f,��Ѿ�\y�@��b�$�m0n^�(z9 �'�Ndo,�,mw�F�~�Y�� L�]PĹֳ�u]�zYt��(ݕ*�W:+$��\Z��pe���M���x�g������붖�ehb��/R1\x)�c�����3yѶ�(w�H�V���#�xl<�=���I��n	�}.�>{E�HY��wzV2{�`<����e�ڟ;�'����׌9��&L���٫v5#[�����O\B_s����>Su�Rf:�/8���w>�F=_�}��9����ʧ���Tc"�F��{
mq��aA�_��k���Xz��?�� *�oC#�A�\�L�R HP�TK��Loށظ���8X����������?��]��-|��y������g����kg�#F%��(�j���5#���Ǜg
\�5�m���^J��Ͽ`�n�B" ���ʈZ-ي?2�i�̭D�W<���h��-��>�G����J2��f��綼��3i�9u�3��!SѢ.�|��`B�����)��6��I
L#k~��9]��0����a	ʚ]ؔ���?��/A�ث�����N�^ԕ�v���,lA	 K��ʋI�wC�υU4a���Y/��߷~#�ǃ0i>�(�ax��@���,"�͌�Y�"���o�h�nu�זN�W�L��|�:�1do��2"+�3
�s>(��d��Q��nY
�e�a�Ɂ�h��2�/���wg�`��[��w�s�$m�/q>��]��ܕ��U41�P�&�L(�u�1���9!nɢU��� H>�6&|=s�.%]�0b��߇ni�k��~��<.����;���j��C��8�<ɛ�'Z�gm~S�;"�z������Z|=%yY��?�|�k�E߁������%�8�t�s�}�5�"�?�L��b!ˡ/	|˔6.Z�w3.�d:Q��OR�.�3-��{��[�n�'q��H{X�������IW=����&����q�]K��&��E߬;
��L�G�{mUq���NX��
�bL�]FQ˨�կ���u�,t��Q�"�a�b0�'�J�FO�T9�~C��^��5���!<R��\��e��A�1C���?�r�ʠTY�a����Pu�G���O��󙒕Ecb����c�\=S��Xwv�6�p7DY݀8�XL,,��T<���j�~+ك���ؘ)N�u	1?4N���vV����r32KZ<j�S��N��ݪG���p���?Ҭy/Y;6���P�~��].�o�LD��8^��K�����3��X�(SX�����N�N��#�C9������]3bG�	g�K+7蘧k��67���rS��P�^��g@v�ɅF��+w�~����agp6,s0��It2^��h�.����\����Ո��ΐ�c@?�5�<��ؠ��+6{�_���/I��g�
Z�3�E>tg��W�jL?�_���_[�1z�c��6�4'�=�F���U�+���8�m(>��jw
���R�c�$�p�V��!f֑-�/�i��f���#޳���B�/��a��M�Y��fCBs��ayj���9[�:4}x��� ���t�j����~W!o�5������ie`�o��*+xK��<��)nu���C*Mz�r���A)�7��(`u�ص����h��~�O-d����(��Vv���5�RW���M[�H�w6��ϖ	w��Ռ���,&�2�_�Ā:����-0p����/.��OMu��WT��M5uXL_�-DC�:�_d,&�9\��	�˿:;�85�4H��½�%�<!�������2Dz|��١I�ǧ�F����r�uU�c/?�yEG��B��|'���9��P�1�Ԧ�~���Q��1�w�h�l��,�Q-�ʱ����B)#)�19�37�\y��	/-x�-�Pi����}0H_��&�����\��]k��-�V�.��_Qr�O��y"
,���/��n$��W����j��TY��<%�����	&�6��Zz��'0k��c��;8^\���MڐZ�0�_@�)�J38�WVX.�qLH�9���c9j7D�J�t�V�����J�=�*��Ȩ���7Ӂ��g��<�����p���Ļ�[ݘ*Žkhd4�,����z}o��"���f8]�ۺ賩��EQ��K39�%屉S�X+̎y'�j!;x%Ps��L�����)i��3�MpT�卷�����݁�	h�>�S?���܅Wθ5H5�\:J@�z�	��Ėt$��4V`�+���������hQ2�o��qv���n;qÍ���$�>�[Qav��ѹ,4����q^�P�;W0����BᏆ�zH���d�j̷.ٰ}N����S��V�}�X̳�q�9w}������`f/�$��P�dgɍ?�h����S/TR'�P���|�F�h⥢Ե�3���R����Lnwy_Q84�/��P�mz�7�8쬔�|�+��8���z�������OOm��7���p�����'�ҕ��8���2�rIl�:;k���~�@���Uo�[�#i ��7Ũ�Lu���v��=�	� AI��H�T�`��nO�"芃V���@�=����yvo֘�ĸ�j_x�/�O�����ދ-�V��Z���H���'�����{
��2x�La�e�%y7>� K}b
�w�Xl,�=��ș���&r�a��`F9U'j�mB�g惊����:l]q^N~��x�pu����:�XJb�*���#]�����K��U�{b+�k�'��Cz3/;����킪����Nbd�F��ZR�;���>��ꋆ�ȭ5g�L�ߑ�d�d/x��q��Tݎ�:5H�ޟr�q4�[ʏ�D�[�&H�#�&Đ��_��n���a,m�}����u�P��Ժ�7
η�ɬ��jL?��M�}:���y~*�Uds��;F�-T��<|��cωt{t0#�K��H����n��uG`�:�>W���GZ�b\L�
s]���{2=�k(u���w�Ї�~I~�E��:�]�	x����4�5HWۛ�|���j��lf<�Ѫy�~>��dw�KǷҋ!���"g��Y1<���s�]��Ը�h�k.�1\��Ԛ�*�&!��++�a��$��_'^ˇ��X��;��K�k$|�!��������f�r7��io=4f��Grap˳��	���P�vUg�{Ne^�����j?��`�2WP�Ƥd�&V`g"��cNk�qg*uv��_#CδW�6��%�ʽ�U������ב�<ž<�M�4?oO��(�[!�~�hMh�ڿ!�u	
�z��W��-��/i�p�oRͫ�2b&��ee�������� ��r>e��,�}Ȝ,�v#�T��.)��k�p����&1f�o�<&{��&�g�y1s��*��Q�����+�{���F%��|�y���8���2��)R�azֶ�'
���Ld6����R`��mR<�q?H̝A�ІV\`dG��<!�Q,k��a�xpV�%Z�;W�?���{F2=��7~KmzRb�����ޜ���󗓍�،�,��G={��:Q^��i���b4���N5��C�8$�g�C0Y�,�C�~��F_1�&|vb1m��*	]�vS��l�cY]�Pm�N�L1��>"��:#��"���/�+![�C���tgwO$˘���˴�7�}#D��f|�9��;�i��D������C�����$k�y57�@:�yJ��<!�ld��Eݷq�^O쥷���&��y ]ߛ�79=�߉�q�|xZ�I�F%b��T�b��6�i�U9�[:5=�Y�H��b��=B���b��j�㡺J8�ۘkȓԊ�Ϟ�R��1/oꠛ�R��aOP�^;�^����ߩq�
���ֺ��$�6"���B�p�į�k���A���D����,��i��q���r�Q�O��r��Żs�Mf[d�`l$�2��h�,�)����^��6Hة|S��Dg���SB̭Y�"X��'{�~��]te�9!|���ewi�fJ��������4��х�ad�ͷ��ӕ�C��A%U��y��o|�w�tC"�d.��&a0-���!=d�O#�ߒȓ�_6������G�vy��"���������Fl�����C� �)�U���/O"R�spjl�Ӗƍ,7g/(��<AW��7j�_3��񅮸�	 ]��|����v�w�T�_�42�YS���y��'��
7\e�n����}�W��ϔ�9��'�����]�,s'�1�"U圫�f�p+���7;	������"�H�����p��o�z�岂x�M���_�mxK��0�<�B� �]B=���#���Ƚ�/Y�؈��GX�L�U�N_5H�]�k�SW?_^��<
�t~�� ���
Ʋ&:-p��u����Y����8�4��9��g֣����0�-��g�Q�?V��e�;��e�:I��do�M�13�����X�~�->�(��=}i��ϢB#���:��̒8f�;�홱vZ�12b� ���b�'r_��+3OB�~��ۘ%�]_�#�˻uq)���H�	��
�������_��ӓ�u�o����3qa�C]�2��a��g�j��:�����{��hՅz��RǢ��L�.��}���%��qxK8��ߴ=~ڀ`ls쯕����Lֱ����O�PxF2������1�F�>�+�mݿ��n����>�Cz�*��Q��$����#"Ӭ=kjȣ�́�b�|]1_m>45aKؚ�[e�;p.d�PͿ�J`O�
s<�@��sO���F?Iz��[���SՃy�(z���4�i/�`F�&8	��'lo�Qt�Rǐѣ�v�4��AeW�sZ1��.�r�����,��O���SC�q��e
��.��n�L�3b�K�񬗫dN�'������?���-�s�e��	�>� h�rڳ�B�XA-�[Y��k6e�.?���[)H~�qׅA*Vv��C�u픝�,�p?������({t�.������W!L����	�Yi�,d9�tQ�����-�H������]�/�}�"GB�{�j���H@�C0�*;g��`�>�H����,�|�Υ�us���W�R�A�er��kעgQ���a!i7ߚ�fZ�v)eK�Y}rE�Sb�� ���T�i���gtE�A�݆�+cc��>r��KT];=�Ox��G�_(���чG�d&p�OWh��O��_ɠ�Չ!���7+ƒ�^aN|it��=��&��V/@x�:����|�T�	�`�"Ɣ ұ�g�;c1�gf[:��_�Ǖ��3��c�-�ĵ��҈jũ���> �SA$\L���ڶ!�az�U�
�c�e�/@��	cz��$����q��e�P^��*gf��x��0u�7�	(Y�N�6̙`�G�b��\��-	�w>��s�: =���QA�gia"Q��Hپ[$m�_��\�xX�y����:���_'c�<%��� �]gu���]Q ��˲ �i���6�(�m�j,�4춇G"�	�&���UD�^���w��{)6���AU�r&��?�E%-�򐣲�>�D��I��H$Ϡ�hl
���NDZ� ���� PK�����k  �s  PK  �@�U               word/media/image4.png��eP�_����Ap���!��	�ލk�q	�	���F���[pw頍�6�'���S��N���\��%u�����u��j*�X�$���������?�� ��&ޢ���u.���?�\�R� ό�7�����k/�>1~ҡw71�	8r��̚:��4��g�?AU2k�&�Xj-<L�<��w
d9�^���l������D�/��d	;O';�(I�o�DCXc:ݜ:b��"��:�$��x�nP�b�q7͈ѧ~��d��/#��Z �7L����jB��|7��'��P\�>��*躵�pZ�[�'lPOh���$���� ��vǢ�,4�O)�:�x$>^с�s�	��/c8q��+�A`,}(2d�p�}F�����A0���a��No��=ÄL`Y����lJXO��b�:�	q�}�;�l$^�g�E���ݭ�|9��!����%�E*i_�i��-C<�H�i�NV"E���-�v+l]?�p�٦��Y��������K������k[��8�-��������8�h�df�ZOO�R�T�qH���X8�/|} ̆Ba;��!��J���	����^r;g�m���w_t���� �$d�r�>�9>>�x��-S�Q����G��y�����HS��B���Z�\>��B���t�od����Fo'�����އ����VX��e��D��Z*�M���l�JN�d�^�#�Ô�btq�P>lG�&$����}n�K�1��"�
�G���_�C��YE4������ٹMZ��x��!�ڕ����wp}3���k�k�E��WMck��3��z2�ޔ��}����������p���q5�vrI�I=�z�T�J� ����k�+��zU�J�����pkt*�EQ��2_�kJO��;G���v��7"Ѩ��@=�0d��.����:a���MPR��j�U^n��$��w�$������!��&66$��٭ރ1BKKK���Pl򖊨i�mY�wY�x1I˗�݇��J��;�$Ah:M�RK�ڃ�t��h����ד��X�v�h{೯�*HMK�"G�455�?U)J|H�����t���C�dˠ��-��n["{��}_���#_���86��=x��;i�|���Eng�:���19��NN�$�2��W�;�������X��+�9�'�d��cN�������HU�ItzA'���M�$�EJ�T�6�ig��Z���
�h窧i�~��Ţ-cZ'Ƌ�}��e���_�J~�P6�^��"8�B;(�.��e�ɢ��"�0%�ߏ�+�����͉�b9.6!�����O�#v�{#�7�N��Ȇ� �^�Me�bp��$�t�\�XЯ{��>%�@y* ��x!U�ƣ�K!!��8��48��%���I�*�i��BH&CQ������.�*��F�t`�{�bC��ݵW�Mi�]_Bf�1G���aR�ұ��K>������+�#a�p�TV�?y��Jxm����z&?GY�V�-�he5n�+�N[�k7���4i�+���uN��ѷm§�8?o5)�"�t����
�n�? ccȅ��;����'Cw�'�K@#�ќ����d�����Ӻ�? 
:>��Q<��U�Ñ��J�bi��_���v��IW�� F�����q����0��Y��#_��F��!?��ш1ŉ�ȉLp�O֘Ƶtf
�47���`�&��ɷ(>�ô`yf��s��^��k�`��p��p	����5s`��=�[t��� ��گ�#�]L�����q�.�F�j���'!#�-y%��_UuBǧ�H��7��L�2��GK�{�5<�k��T!��XNwn�4[@Qe�alq'�X5�ZI�t6<ʆ�
I_�lok�-�&)d-��'�û�?����>[�g�'�>�?� �b�<�B�7���:-��)Iq��q)��z3����<t)Q���H��}� e�xU�z��+���=O�#��!l�5O�o�� F����
_Rg�j��LYE�����Uԧm�~�G\H>��Dy�]w��h�|=r�� ,�*�znhtLE�no�|-��6#S���Oa�1�A����
�SaW��.b�������U�N�ږ���z�߰]���#=�l�J�CZ����q|g��w',�s��>���ܯˁAn��)��x����|��޸���?��,g�w�
�3�2�CP u��B��v�!3�o�]�|w4Qp��
�2i�o�K���-#�\�O|`lm��ԕ�5UI!�pؗ�K8e�9�Q1��u�֌1xx�g.����@T^2U}��/��"����\mV���}�(�~
j�,�,��z;-��2�)Z��i��7��6�n�5fF$,�hcŎ���H�~�>!���_���Z÷K刢+����B���o���k,�]�KVP�t����N {!9�'����Lm���e2zU��3��F�Có���׻�mMnʵl�>��P���K6]).۪Z?�,lT��_�.�V�QܸSq:v�����v�*q�"9��'Y��Xw�{!��;�F�xr)ʟezᶰ��,�U�ߛ���rI�Xl�ɋE5.����~�-g ��}�W/�>�-����9C��:�?��e�9����},ܯx=�C���νȀ��Q�yy���B74���J2?����m��&Bމ��7:�o�v��Rw�r/jF�n�X��Y����rN�Z<j}ϑ6K�Ků]��6�:�*�9Ymz���pl�n/P!DXA�h���v��_{0 �Ky��[3 �)ϩL��R��h���e;�3OJ�d�X�y�7�cFtu�Dy!irH2��*�ʄҎX�Rw������a������MgU�!.[��ֵ��1?�q��s���B�&�"I��?��Ei*�Z��K�*����ϳ�����:��9�nr��Z�?�A���S:�	>,����z}�V�Bɴ���1������=��yg��[;y����W�s��ڬ������^5�C�s��9v�&C]�'q�����Su�d��H���9�����f,U�P�݌����ݝ��:�j��'��޻[�P�iu'��1��F�Q�l�wS��"Ƨ�aB��ǰ;�o���X���?�1�6��D��j��h� �)��{��<�ýZt, f;q���sAmޣ��
l�'���Ǭ�
��cc<j�`� z��h��:��2]�$����l;�#L7@1��)���M��!���X���MNv$�:�mUy�"�&�y�2҇䴝&�4�*�4"�?�T9�}cH�ڶ[?-9c"���ڥ����d3W*m-�/Qa����V�p��Xk&iM�xvz�rBC�R5Y�j9*�9�(�"���D���O���;f��"�V4�Q[�&ކ"�<V�X��MR�S��$੶��K��)@����utn1Z7rK���.- qؑ��4B�=�N��}����}��z�d�M�<��S؍��/��٪'}A�5�O���i��5��C�q&(�|�JF�?���\�:|g{�}���-���i��mMˠl���
�����L�]�^�R��M��i����'s�Z�wT���H-�Y͒G���>�&��y�n���I9)G>������_c���TG��B�n��L
�!����0�h��&\Vl�r�È3����'�}n�qy���Λ{g~�u�H��32�?�Q�-�@�XWR�y(�J�dڡ�0u�\"����X��X��^ۑn\�AQ�W��Y�Ͼ�O� �v8���C�����>V���f���
~�밟Z�dP���کv���;�i��.M{#s Y�2��:�%I�J���9L&=�E_-�5��*�f;8��-�qlOc����B!k\alV0R�ǳM��D��Ѫ?e��k��%�˛I� "�át��up�w�@X���CƲf���F����pk�`�l͖��DnuK�O�C��Ũ�u�N}��g��<ʅ�c�W<NB���_F���)WaU��t��P/N�IJ{�vX#���"C��{]��^�T�����X75���%\��3C����{�\mjR::���1^e%:����k"9-1�����߮���Q��ϕR���4�����i�}d�w_�Q������^�<���H�W�q\�Q��r�D8�]����i����'N����v�[EI�U��^��pS��u�I�Z,3��:+~��[k*푎/,��5u�%e0'j��z`3[�w��aS����[�x� XYpx�v>�rO5�w}=��uA�_q�j�9��g��9��yg������쳊�"Y�m��f*��E�V���-?��@�a3�8�?&�gG@v�L�C��$�̴�����	����TƯ�ݏ����::��R��gY�P:{q�<���$��ʠ��J$R��TXq8���&3Mf��8v��[�.�0]�fur�=v5��s�\k����?B�Ow��8u�� F<X����>�m�--'�s��,$t�:BQ��H<��������cF9>��3��'���2�jF}Qa,/� �V�}��,�� ���G��^<2]�;F{�V4��=�]\7���M����nc����qUI��Nb��͟YܺQ�%�O~������Sm�$�Qڕ���3F"�3�ESOJ�KV��
����c�)��ųw��ߐ"u�~�6Yb~*��A��%��]e8�5�\������D<r�����W�.�e��c��n��B �QK!9S�H��J�� ��:��M*����A�0[��Ln������0a�,��>Ս]TII"���
�$��|�m����$$�/%��n�e��xMH��<�m6���|�ݒ�a0���I�M�����u���9���J����l���>�����7y룕����5���7荔�u�c�C��Cw�z}��Y{�SM�K��v����*-�K����m�+��h���m���ƹ�N*'�)�R~ոS@cFk˺�֝�@��?��7f�e����� �!Λj��iG��GT�D�0:���j�@�L�>�1|���ѫ��ps�7ie����l'֐���;��f�B/�X�	��� ���L��ʭ�@��V���L1ojr�c��������p�f��4�Y{�,�X-��_�`wH���1�|C1���U7�O��"�{PBGu���ʈ�dCm���85�4�z��gy���?����j�Z%W9+������P�H�*��*géY'����Q6�W!��!k�?�g������ ��uÃ�VZr�w���+=m��PO��g$��갞u�?h?���|J�8�kl;�����=�m՝����p�&�i̇Q2�pr�J6�hw��I:��(��݈�Jf�"��O��^9fuy�k���X�x��`|��VQm7��S���n�4�%�m�>DP-ך��}�t��F.Mz��?O�[V	�-�]G=rD��%Q������U�Z�?,����_/p�v:��e�Ӄ
z�{'��p��Y��\�^..�����6��]s;�į���a�����~{teW���E�,�w���rUx&�nr�u�"�������D8��?l5���[��p��6��м ���Dj��.L�JɕA9�������#�����8o��'3�k�Q�ϢF?w����h�6~5(��x��g/����3�	|c��J����Q'��[�x5¿�S�$w�}�(�JT�7��H�8n��M�z{(�Ҙ�*��3?�ͨ-5�W"�- C�P"�s��0�հ����_mE�`�A%�}��W��@�z�8eK�����I|D^��*JN��6���_��;.M�Yss�Ȍ%|�p����J$�&~vv��;|ȅܕ��i2�5؇���
\�����9��tb7��0U�x�kŃ����<������gl1�5���EPI�>}�੔,,��,
����(�s�w6���qZ3������h�Y���z X���P���'��]���}hʕg��P�O\�m�Zx*3���K!F�C��Tݣ˥Yh���ܛ�mX��r�h���ffj���m5��f�P���5k���a�j,�IHm;}i���6��>X�t�z��G�o=�� ��%�Y��RZc&qG�P��e��a/d(��Q'�����}t`���F���߬��S�'��h�X���5+��^K%x:��w�+m4�,��Z���a���̣}8{�Ê�[5C)v�:������Ni�O���g5^#��^B?���'�5�F� �d`������?2�bdɍ)����z�:��'/��;��r�h3er��ϐ�$�p:}8?h�5A�z״�f�:�ƻm�8+:���e�}0���������b{[���ᘬ�?h��(`x�FF+�H�Uj����>�A�#���&���q�Y��OM� �:�jc/743UBm٭�tV�ֿ�[���I ̘�N�g%�!2yZg.>܍\���i�#����d�Yd��5�t\�16C����1�_:���j����Fj��A"�6yfJ�������8+�m�kzg��Vpj�ot큱�����S���SK�3�˽���R���ʷ����$�l�x�Pc�@؄�'J���ʑX�􍡪`#��#
�X��A�bQ���o�X���B���(X��?A�ł��
�`�:`y��6D�֩ՂZ
i�D�l߲�++�ZtDY ��ؒL�W��	d ��ҐE��V�P�u�V;"�C���To�9����ƶ��댜��S�� �ɗA�]�ꠛ=CM)0ՒY�SW>��r=��
��y-"8e�m�����qi{�H�rN��bL�g�Q�ȣ9�9�D��I/�fF�L���g�����NR"n�F�Ώl8�'�~�p�e�LS���1P��u�dG��2�;"��И� �6�U�y���\)�<��^��t��24'b����)q�{?(�3\��'`V�������n�a��yy���*�E�� �n��ǭG����*��}xîK3k?E]b.����ob�ϽN8�����@Dx,nc�;� ��b�S�tH��*g�O��xa�̿/H���Ӹ˾'��`I�T�~�Q����Q ���ߢ�9��8�Ȑ����)�>R�Gl{���35�^��k��4�iE�m��:Φ]���״��=-{/��]�֣e�J��|�S>��^΄���g��?,_����8��r��h�pݺڿ��u�e/�$|Ngլ�o|A|ځ�ֺ��G3�8S���x���~^�Iꔝ�-�<6�J���u9��xf���*4�F�%���Ąa\�Xa[C��$��Q�@�P*n�O����3F�_�-"�,[,�:��V��*�z
�c�VyeT��.�żi��jEo.�\��L�J��)�+&V��>)7��k U�����p&u!�Ԟ���+g�H�:R��_��s�7rt��D�k����b]Su ć����<��X�P���˃�]��';������e@��L.����1Ӂ����Q~���mː�A>�^�B'�Cm�+�R�i;(/ҏ.4+�0��$�s�ǅg�����cqEin����Y�5�78�
4��-�����[�o���!�?d���Cv�+���6�36��+y1�0�a�l�P�^R �xŕ���z�����|d�x����L���`U���{WG���+b�$����������68б2����W�X�,�����A��7M�2L�	����y��'�O{���ӣ��ʵ��1��E�ሠx���٢i>8�����05j�ZZO���Y�x7H6|�x���,).<? �1=sng��P-<���H��k�������F&����Η�q��.�߶S�$�^�q�l���ԥr�5CJ�qT$�(%F��m��;����	��*7L�.�#x�����>�B�pnr���q�: ^�)!�������&��c�5�ğ�6�|����ʹP\�9;�"y^ׅ�)*7d�z�qU �X7}��-a�?��+�"�]2Dw;���*��H�t}?��I����|��Zs'+����o�� D��I��j��<�f�/��m��ˣS��8^��l�܃�D���l���i{s�$o��Jt~V��NzX	�obcCwF���#������
�ӝ΍0ʡw���Ϻ��!���V���X�0��.�o|F?%�s����ܹ�k����8���%��-0X~�\n��c<BO��m�e]Y4�r������+�q�%��0��@}@�0N�ј� p�lG����+S� �R��Y�D.v�bDƈ��l�-��?�e����qm�Wm��-�g�� xt I�
SIZkAN�~L�������[��6��+^	TD����>2���q�:]��f��YZ�QW�Hj%Y��C�(����H'[���{�C:��i�פ�d[����2�*im�0cM�=��E �K�̂�dm��j������<%�2)�9%���c��Ӿ���@nRݮ7�i��m�-�������E�lz���t3y�z;,�G��a\��H��1Y��uh�N�l�i��}QWb?mc�4Z�f�Oq�+�7��㫢"���|�?ay\fX�6� �Gb�nOHI�?W���93�T�-.�v�>NMЁ|��`'�V�1� X척Ew��P�`ƹ�ο�,ov�&��f[<������M��&u�0�R4�'X��C�7�#�z�Ho�=��,6U�?g�:%�"
G}Ε�6��1����79d��6L��mr'�uaC\�K6w�Bjf�ŉ�)��]P���!��6o��ղ.>|�>W�����H�"���|��*\���(u8���g�J�҇'�-�,ޙEWX.�;���ֳ�QO>�j�u	dA02㒊�|`qSG�N+⏖���}>9~�E-;���՟�/���C�xs��H�!����������mk9p��Aa͘l~F��%z�W�B�,έt�>����\�-���a"�CW������sV�%�c�":c��Z��䲗����L���
��tˠ�P�x���X�=.
�[��Nk�\,�^F�G��Ц8jh��ҫ��$/��)�XJ���La���7��,Q�%𧰂�Q<P���kl�Ӆ�4���`��VM�U�W~[��"(X�6�_��D}E&�D_K@P-��%2�%��I�j%��L/WAgy/� ��L�/�+�8����� �қ�{���Ն�
Ů��W�������o�f��ڿ�G��Oܬ?e
u��j�@����V3	�Giy~3�wM���i��`҉��)Q�O_��yAǔ��O�,��igEc��θE>n�������m<? �j�/�����o{�� ɕ%b�7弩+t1[�؅�>��C��h{��M�"|9��3�d�!���N�Qۤy�D���%92ĲD���>%er�e;rp���>�s8�a,_�޷���JU�)���9�]�/��ڿȰ�7m�*���ِ�����n=�wp��Ԙ7�K�^�;�	�+0k%��7U�2�mG��)�S6�V.��ቑ��
���F�Ύ�=�-NAN�1,@fI�z~:X,�@`��d<7'�e��Ϟ���\Q�}y\��H�»J��}���k���bA�����CD��ݭ[x.��/ȡ1�����ѷp4c��1"��JȖ%��w���������W�zP��+����_�;D9��Ȓ<ƴ�?GN���a;�%��X�?��*n�c�ޙ��́��$�H���0��i-tR���d�{(l���&��wzw/��a�|�'n��J&�pΡ�3�K =|D������_�b�|��(�0��Xa)b_�bz��:f�Ik&.!�ٴ��=h9J���s�д��7���Tz�t��d�SP�e� ���yg����VWۂk�$;օ���5���|6Q=���ߐ�M���ss��F����J/H��J-Q�O��:z�-܊���0g>P�3|�|�s��㘭�������O&�D��+h���!ܷoY��T&�jy����> �*+�w^
����o9O8�QDD�nS嘽.��ݖ�1�DM��h��"����ȑ�	7[��������YAݶ�8��4�%%b��v��R�ez4Ƨ�lY(����T(��! �ܔ�?�1�R�D�����&�{{�U��g��������n��wT".Ϧa���זpShf��ht������=�i��^΀����o�����#���΂�?D�,T��څ��vJ��w��|���7�
��9�>�U�.��v*�W����>^�ϤK��5Q9'�`�sF���[ m��Ң��E���M�g}�����a�A��"A�p�iV2�\K����C�珎�~k����y�}n�F��ECѱ0����$'�mM��v���p0b��9�V�����9<��A���s�1���R�Dk���+��j�}0�~��>����%�JАB}��Щ���E|��|�+.5q�9�u#���?wu��a�-����h9 f�y���"�:���K�j�.wS�T?��'�w4������Ђ.A#��W9`�!56,:
J���p�(	T5���SE*�+��*��0�����׸�x��?�Y��N�������>���w�u"�s����p[�K{��� 2�y�NW�؎ �~��\,ˡ� ��>v���4�Z^Z�f�8��t�@Ǒ7Y�[M�#�!�����yAьť��^SΖk�~��������@�2є/s�_M��Jj��˹����3��Dl_���� :e����#��iW���3�	��d�`j�k\��5x���� ��>~*�� �V\�Ħ��yS-��~�� �_�G�-u�IV:��M׌o'��Xp��C
:�AK����#K��"�e?k���9�Yv�����:�|s�դ9GGym�c
iN!�{�j�����)�(u'Ǩ3��8#~�vr��ډU�{7Y��c�~�ƭ9��0�N��yu��=�T�a������ � �zo�ȭWҧW�%;�~X�A9�wX)Ѡ�u��N�����CZL��=��o�kJ�؇2#< )-O��6V�$3F
M{+��2�j��g-�-+��n˺޸�ODg�b|է����FG��1��\��[b��3n��$�m�Ϊ�G;�����D�rǢ�e�v�����6�[��ѯ��Fa�ᑙ��t����s\c/4�d�<����^Ib�8}##�;��q��W�A֔U����.N��̎=nF��k�%AK6sMu&�#2�֎�_�-A*͹I��r)���*��<�5=���i�y��"���/6��cʼ�ə�X��ìB�V�x�M{�$l��X{/3G@WMm��;%dw�������#��J'�OuceO��]D}b&oJ��������37v�FBq� U��bJ��=dp.�7��N�Ͻ�K��nЬ�41�3־���з1����A���㩒���O��Ň�_���L0���٭ �"�����uǤ�
�?�V�/W�Ѕ4�������NH�g�Ď��j���ۆ�`˲�O'8)�:�J��F�M!$�i�''7*�:�|��8�S�,� ���S:؋m���爧к�-'/��BX2e&���bNk��C��C�V�N���2���9���Y�5^��˝D�K�����W�Z�	A=�&�o��W��5�ĺ��W��R����]�,m�H�W��\{��O�L���e�<�S�=ܗ�� ��%wŎY��N&�W�|t�uN�b/�2F�s�-�����f���O�l�-���_�[�eO���C���.��r_�?�UP�"���x�lS���v���3�sp�g����^���ʪ� S�A�{x��p�-�|`�m$d.��1jIi��>�%ӧ�J%��i� GL���^Y~��������L{"H��6�Pd$�]%:�������Ҵxv�[b�-����l���^f��5�\�,��ɮ�x�^���z�4�Q��F�S����u#'�J1�����2�o���?>�
�v��/*�;�h��81�k-g���D=�n�0�2�OV�������D̘����&)1���f���}+���;� ��$$1ߢh���R�C��&�K�-�oH�*�9��w�$���F�
�!�g����LA�,gǍ����q�0�y�nf�_'���$Ͼ�����[ �X�Ju��UߘTq?Y�81n�0S��`%���㉖T��Ǽ��R5�;-��p^��`3/���\�]�Og{�Ժ�f�|�Z[��ڤ-K#ͅ9a׌�q�uE�t�J5}"��3�N�
W��kX+�����\�z����=���=�oZ�ehL[�\�=E5K�[J��u�����ի�Hs�d�f0͕
7�].��S2J���}m�Ͷ�~_se�lH�4����5%� � ������I��u��Ig�C�Nc�U�s���G�R��S>���!A4^���	j`U*�
���f9!咨$kĘ+"�D:�9��SO�ߎ�	�#`Qj�ͳO S�Ԃc>��Ҋ����e���@0�o[��k�cǉ*�U��u�G7��p��2Ęi߰�34��V��Ī���(nE��B�Ѹd2Ll�e��C��8�淛�8�&ҵxor�O0��׵��-��m�G8��M^�B��M�9��HأX�?+9~ك����0���;����9�������ײSQ6�}�6�LU ���V=�C����[��`�y�����ޡ�3#Wa�h��
u���j*ǕvV�Pv}~b��X�`�+S����wW���X��8�x�f?b.����Z����z�TV/)=P���%:�3G�e���Ɓ�I��d�	�ĤK�p����0��À�!��E������R#�,������+4��,e�єHWb<�US �n�i2�����;��腖QV����K������x��9�Bx�^�̮�H�+w�խf�Bǝ Z�r~���������kzO��Ƒ�[�1��G�{]��&*a6���/��ҫ	�rRZ0�ۊ�r��y=ؒ�d�7-l�p~|��K��b����O]���=�V��V�
ϕ�����ӯ[�عՕ��$u
0���⯏H�X9���i#ەC�m�sx>�ӥ������;��ݽ���.~ bwTl^x8W��cqe2�#ؽ��p3,��Qd����?�E)�/.����^���x@0nO��I;��;|�4��ߞ�A0J��`��tZ7� \����'G*I�=����9����r��Kק�}��&��~��}��g���s�D-GBC{��_\.�q�1�Xit��ō���t�+�xk*���M�j��k;�)kЌ+�n�R� �a�{�d#��u�C@��j�18�f�cY����� �����r=3���'35��óN����J�9���bi4��Tx��A6��X����+�_��S�WY���F�U�	$6�:��co�*�Qr��@�*������aaG��߅�o��Fu�C5w9J�C }I�ȇx1Br��oR��Q���RA`�s�m]���}ײ����?��W�D�3�Mcl1k�ȱݚ�#���	1G���EN���x�NO���xC_ӟ>��_=�)���'���-��C|LD�g!;O���3S��):`�`�'��㌡3КdYt� -W��.��\���Ŗ��G=q���aXU�����JQ��G&�a�L!��ܶ�1?�Q59���c!3'Uy�w�b�>�ظ���o�'�ƀ�X�J��p���������c��_Ias�_�%�������b|�+ QQa�T��#I�[���e�J�u�8�À�ON|�a�	�6g�[��A�o�>��"�ma��z���\Kߎ�q�Q��Z�W��w������df�(��QuϮ�Yl��n��\����X�䘣y[繈E�9����/�;!g�ɚSVJˡ� �&�m�hO�aB��׆�R��D��m����̸T:%��X_UH������A8B�w���yɞe��19C٘�q�Z�R6f�����dL/�:���ⴵ4�5 G@h��( ̗E\̛��<P�X<]�RR�G�0艠���q0�+g���e�F>�)�Xo�}���*J�fU�����Zh�XW�N�����b�۾�2o�U`�cpm��u��s�vōV��
����f"߹�/*�VO��$ɾ�j%W��'!���S�_cH�n�Q��Z.���:�����ﻼ�ş�]HF*�sTc����~��9j0͵y`0`e��Sz!�&�bs�7�!��z`�aY�
��*ZI�I��c�J^h�v�֚-���T�IGԀF��xKMvv\A7��{$����%�>�v�D)Q�,]�#� ,e��`��gTV;�6T��;��p�Hɪ��t��Ye�Y`�c)����F�٢���͠K���/߉�ϥ���#�%�C�u6�J�}�/��X6c�Y��t�}L%h��S?
f����B4=�E�`�6�~�����|0kh�$=N�L��9��1�Ҿ#aJk�69OG�G�O[`�wW���>y<��ݯ�|)c�L��I�UT���aq��1�Z���A9��( �2{��kC��$��f}��^�)��ޅ|��1w��뤎�y� },eo:��h4�
�\����2����'���y�C���#�J�X���ҿp����w�TS�Sߚ:�h�'�g���D��kf3�Ne�}ù�`-�Qk}[8���̜!C��W���E��rvG~��Z�s�Ys���W��lERtu�� ��~=��%͈��/��H��h����N�2~]ϩ`<�y��i���Y�pV�vu�i�Ū��S���gm�.�|�D3�6׎H!�Ϛ/�/X��-'$i
���0�}��3a�V�r����¨tCJp%|+�3�Jc"��|@�~���u���9N���s#���M���L���Ӌ�[�Ʒ�$�~A�=�N�I;S�0~�[mv����&c�O����D�_0��o���.����L�� ���P�G����Z�)W��I�g�{����g5��hv�+�6�(|\�\����^E�����쌡��~��uo��ζ�����C��;Wp:T�TlE�{2������`����!°���K���lE$�e�\WT
���?he��u��rJ�|ߗ�i�B��ۉ&%��T|�Sl��q�C=F�����vo��;.�ff\��N�R �_W�v���4�����[:�nL��p�5��]���0��
���˾o��$L�b;Qӳ܋rY,,�����:9��	b�r�C�/�&4��M`@��3p��S���%K�,&qsU�,�"��ЭFʔ1�)m����v����?� �l����J�\�
�FN_��ė�Ά�3��)s��'���}�Lk⢭�OɌ��_Vg.���b�rR�sUv�������:�WG��a����	�Wt��9�x�.�?��fc�ǖg7Ƥ,�r��@/��ӋE���=�b������X�Ĥ}�W˨D�w��n��k���U f�����K��n����W���{c؀����% �ՐC�Ҫ����H�<*˙%5�7�-o��js�]��b�fSLe�Iv>����I�{�Y����)K;��'�S��3���"���D?\��3��r����wA@?3�fÎ�hi�8]�UЀ�wx�f�)9	�SM�B�!�����$��<<y��+r��7���4b��<�Ų}v��yۂ��9℄�ZԪ9/�K�Pn�+$�@��u���l�Ȝ�`̓�2Ӑ�׀�(xr�̣�Ll5��IE�p�d�d��ۡ:%�N�ΛWN�����?�A��D�h�����'�n�8�7�M��}	ߗ�u�2Y��&do�6�r^��O'8o��me�;�ǋ-eu����Փ��Ue%?�ծ�'dBKc��1bR7���\��^!?�,eJ�.mq���t�7^��/>ͧO:Ƕd�&")!!��X�tc���k}ǎg�t|#��s�9sqC��9����D^���|G  ��r �X�

�N(��BC�#"�!sS
�?���W�AXPE����p.�.�5A�`>ui�[�6���ܾFTfM4�q����[�Ck˽o�$m���Z|�7�����uB�@lYc���LR�,ϳ��Y�v;��܈ED�O�r�a���\����ù�%e��M̳̾$�W�+�����e;t�d��:z�T:�^d"����9��x7XɎ�K�����e���W���_6�"h���'�A{�b(��䪐J�*���VV���2lF#a0J3F�q{��
�TC5��˿WH]����h�����'�	'�`��Rp;��4+�΀
��ܑ{I�*�ϩ�q$ۜdA�ةV���Ӵ?'b�;0����n@ �ģ���#J5�#Q�K��b�;��{�EuɎM��M"h�5θTƆo��;���9��?��.���ut�K8��!B�>Y�g��r��x%-+��_QUXH�ѣk�!���*��m]w�h�ŭ@qw�����!H��Lܡ�Cqw+���w��:�Zkv�ݮ���:��qAB��y2^��q��d-�m�>�����[��Đ���ڜ�u��Q]ݎ�$��q��X'��5"��ӻ�;RBBmd�<,E�7
�v��hq>��C���g�f[l��������a֢�OA�92��F����;����՜�7��f/�^OIN�a�7XX��˜s�%+�-,Wt�ʓ	�)�;��C+tJI�@pN���*�R�M���'��s<ci�o��n;��ö�[������U+OQ����cV�psR	?߮n�`����BI_�.a�y:�\��ӎ�񊧾��C/�LUm@Ĩ�\�t+p���2`��yߟl�y���p� ���L�%�1�F���W�0�ɐ��"ո�Oؘ�)s}O���l�< l~�9�g�8�TN�Ds��R8ڮ�c����X)�=���9�)>��J|��KZ!���	7��h�
`S+១�.ͪ�z��*�34ֺ�#�0���/L��T7 ��|���;����iyӌ�ɾ�<3���fB?�Z]��l�]G�����`hlњ��\ź��T'�����mI7d��/Ȧ:��@|#����|Gg�(RD�T��26���<�"�m`Y��_"茶)��dB+7��Q�(���#��������nH�_�#~|��9r���������{��k�����nn�A菘��}TNPE��ns�{`��L\!��h0ϙ_�Vx�6����"�'`���ӑ��W-r�ﳏ�E8�n�6�H��P\
ð(6�XC�K��}�}��e�>r���>��	m�#X3�q��.���"�<9ȝ��yp�7�x��l�?M�I89$�r�5��K���ߋ�����^��X6�ۋw3/�������a\9l�P��2�dhSxi+���L�z��
�c���`�%���8S������erk��ے/�x��������~LJ�&�Q7O5�������3�s��a�#�h�Ba��M��P�̭�2}?>���1�����Z�K�Y�|W ��ԃ�x ��Α+�6�tj�*��6����
!��I^���{�Ǝ�-d
�EhOf��A�<�F/�B��&"O�c?f,��拫�F��VRl�Ϭ�OM������ޜl�<�~r�sr&xx�@�	S���q�jO�|Y�|+�������l��l2��,�(�"���s�So�X	���9������;��_���������K�臺�	BIZ��[bڽ>�\�,�*��6&ĕ��+��U��Dh�&��(���q�������9�~�PN?�>z�̌�v����9SuD�����'��,�.=n
����d��
�vj��7����0�%"�'����2l�<�VCX
E6�d�'�C�1j:����͖|��xz3|џ�tu���O�r��q��ȚA��=52�7�	���;>������0��i�j]U�9�ⰲ>,>y�7ZO}c�)�����y�H��E[T �*��>����Q�N���fL�n�<��=v�e_�����N���.�ŭ�����B�YY�9���&�j^> [�t��P�v���#\��Tw�K�g{H�봓I<n��6��ܭ�O�:��2Ii�/dӡ�'Xr8���{��D�f�<�� ���q��K�f������3բ&e͋��K�^�)��l/�2ЭvVv��)U�0��,�ۧ�]	/���]+ ��29��V�%g��	��҃�6@��-Z`��4����X�Z;M���J��/!�c⽭�Iw*��=)�K��^m�H7D*��-��
��q?�_�v��+B����o��s%�"�:�-�O���j�_,�ꃧ�,7����t���v\U����[�0tج]����ʚaI�ȏ�T�^�Q�u��,�����N��%(x�o�7�\�������RĆ~�hUb��y�_HS�[i��bJ>z�x{�٘s��k�2��q����a���=�8͎��X�bX����mI���g,_�	�EQ���`S���+�=��/�1�pW��1q��
7����īGG\Ғȁ[x@�&�Z@�#��
Z��'Ɓ��7(�Z�d���]�ƺ�F�SLE��rͣo8������2鎬�(�+8��J�)�B�K���H》Y��PQj��hq�v1T��>�	G��IP�f��9L���8L��&}�����5�K0F�g�7t/Ѣā'.�����*3�Y�#�H�#���]�3�#�%]�"2���x'��2w/;�va�J�����^�P�*x�0����ߚS�&\F}��k�7�2��#�acFÛ�P�Q��6:Ї�u��q�!��/�;{�?bL��[U�p�$�-;��@jv�c�����-W�~��T�vF�ʝ��h��L8ˁ�~@� qz #�q��a5N�^�p��K�_���(���)���>�,v�gr�%r����]�,�nǺ=�a�Mye��`�!�9}�j�N�|��N�8�$.T���Q�Bo�o��]�z�h&ҟ!k�-� Ͻ+�.HEc��b06�l�B�������� �{w��Z�m��uI�������������=�I,?��h`��l�������q�s�i�^��Iۼ��|T��V���m.f�=/��| rLw:���x4:�n�F�J�>��J��R�h�E���������^���%
���~�c�OВ��}�6N�C�c��.�J�{��q:Z��Bp���	08�JZ�/��(y	ӝ��]����̅�`kމ�8nڍ�6�k^�ǭB����cm��`��S});���f~B��ª�t.�cl�_��yG!������0�_� �k�Ϫ�.v��/5ب��֡����_�j��V���t��Ll,�)�ƣe(e�̒W1r�<�C�u�$�+������v\>j���|x�῅~�˴q_pF��A[�}1�+ye���u}��-f.�8�.[�����C;�x��Kb��h�ӛ����g��	R$y1G'\)�7Ԃ��Ϯg������֟��Q�W�S�:|U`Rq3�����A$��+��:b�t*����+m���┿*�)0��S�D]w���u��*2���67���X�s�w�E�p;H�P�:��o��ąUA�L������Ҵ��%�1s'�J�V�<���4Ғ��ٸ�u{�#kTX�)yu����A�%~�su�Ȑ5��@a��5���4eb���~k����7%~�dq��^ޜ�o����~�]���Tm�kO�7����C�N?Hk0d�w�Y�6o1�j�X��2��.�{V�:[�`���`3�ӣ�M��OQ+ =�$/P��Lf�����G�k�,-�N���y����o�⽢x?�d>bZD�������@h����G�`H[@AB4�����3�u����GKu����_^��U��9)噜���G�ݮ�=}����9�)()��^�Y.�.����$�K������\��c�S) ����N�
ߙ�����D���Dm��?�����_i��3ѥS�5!מw%J��/Ηj�f�U�ˊ%��t(3xEU��gκ����J�V|
����-[��e3f;&�#<cB'u?��cZED_�s��`��\v�M�G�]�g�5�|׌��X�R{���
���	`�VdC�rI䞏TEjdX��Qo1��\$�j��4H	��y[�LEf�����!�{;�ܮ�>HiYҒ�wLQG�%�r�Ő�}r�kF�Y�<{�'��&�׋��kͯk/ޗ���p/�OЛ>�M/o��M+�ˎRҸ�-^n��/f7~�H'{"_��.Y�I}�LH�L��#���L�d�2٨��i{�3J�G����L��`Ú��6�uR��K�w���c��5�}�w��pt��~A��}��M�7]��o��=���Y��c�TNu?!��W���D܎��G+�vIo���c�p
@#:��tS\��bM�zrҭ�;�^�շ7@�%������(�IAf��kv�kIEF��)�u�H�dl7���b�#��*����}�Ζ�Ƅ��*�Ob��kو�J��������T���2�4�QJ]�<�1}� G1R���B����s`��_�-����r�K���]�i��[��t>���PGz���o��C�����e�̒	d��"4���4�C��J������!�م\xp�>��;4��*���aE:Kᨓ�t*hB�L�ȼ�'�Ɣx�T��}������%�Y>��T#H4&�=S>g9tv�=���AJ��HN[
�+�����*�[p�I�difs3R���G{N)����G�&��X\4W�����-$���x�Ah�R�X,F��[��r�Et%�3����g�B{�R�yuI �k.o͏�Z,&�]6�t����+�`��K_o���hM4�Fȑ��K�� ��C���/��[e�ZrH���v�vSٟ����~��'j���GW���r��}z���M�j{C���O��R�^Wh�����
�Z�k�ǭ��`>a\��
흣�;v�b����̫�����u���,	9G;���.V�]Q��Ҕm��J��-��2�#քvf�'q|<g+-fZUl�&!;��r��q�H�n����&D4�f��eA��G'u�E�K��w��-��/�ӵAw�ǌ��v�Ǡ7��y�]}�Y� k���9l������։�+�D�:��f!x��Y���	����¤w2-;�c�}�\յ9�*�p�sM��Ǻ��K<�̫>����0����gvP��A/%i��C��:�e!���HUW��{�s�[�&��*�z͋O��)>�ُ�Ul�O�2�+��ƣ�}�0��X<%�]\��DF�m����Dy��#8i^�s��^;z�?>Ϸs�cg6���9�M�,��&���9Zȴ���-�����1E�	
����u��Yd�q��#(���QK�����2�;�������U9&8���he�+%�!R3:˷�"�]�`���'Q���Y�=��������<�|�|��6���aI�ët��yY~�4���H��LP氟�wFX���A8ǩ��v�ģ7J�ɑU~�)F(\���9��j hk��f��{���v�{��P�8��}��HoW$�,��:jA`��׽jV�s�}T�T�7�-D3��%�����fQ'Y�J@!���dvdvt�K-Wl�IZ�:%�hJ�
5Xa�w�g��(���Mۂ=OK����Owc�xK�Қ0�}��KU�7"�L-\�m��l6�u��'��N������6D?�;���B8��a%~6�қ	N�T̾��R�-|D���2���E�4TI��a�˥���bs�C�}�A��\��
�ۈ��B�s���i�h�c������c*��yr��I��䌞�D=��0�Dp�n϶q�dЗ�CÁN�Fg�gP��b��L9��`]�ͻΝ��=���p�OM��j���T�5�J�R�N��^�Z>)���1e�����_}W����]Y�y���`�����*7�h�.�����o@��lx�����i�� �9��"xS&z&��>8b�o�l��8��w=f�aO�~�~�����q��M`�uT/�#�`|�7={��E�+��Wƶ��6-�v�eȸ�9�*A��F�7w��8��vƶk��I�5+n?�*hb�[4��Zu�b���>����Oo��v�41��D�#��+���oV~M���MI��*=�FbŮ�^��2����3�]���Ё	,��u6�M��[&� �m/�+{�ػ�{��>�:Ks����Π��S^<$KO18R�t���'����h����h��k��Yh,|�3�J(���7=�����~G��5�tD����SH�A�$U����Ge�w����;��(�Ȓ�p&���9���ʢv�%���S.�n�����3��z�u��g/.Կo�5�S�Yd�|��X�kqz�`w������^�:ܯ���R`"����z����w'�V{uq�5<�7/E��Z	����g��+���[��.�\�9��>����/��F9��Q�)������1E��8���PD2V� ���T6��������4�^���[2��N����۸\�]�MTri�s��Z����f}I�,;��;@s��q�<��ΓZ�@	��]U���q�0��Ú-�V�B��8�.�[k�ћK��}�Xa��OB�@kl�o��ƛ�4gR�E��PI��/��,&j`��+n����C^[a�U~W�U6����H��@�/����`$�;��o��L���0(U��`wsn;~*���a��������ӕ���䵔lq������X������\����|	�d
l6�r�;&;3��g��*�e���f�k��9�y����wR�CP�Z�P���P9ϡM�7D|�M�2�_�f�\��'�����aS���	��Ť����?��X;����g�M�3G�<���m�U
�E�7T�g�̑,Зe_��\�%�S/���Dj0��'����𧆑�ƻ��j����ghxFRPf�{[�_Q�Y�c"��'n�ZӨ�z-���^\�-�BA����8�;	A]�*��4�r￯,S��1�\��p"O�ʧ]�+�m�.Xݥ��/|��S&�5A�3�E��;��b��hꗪ(���d&�n�bFG�*�b�<��I�x\GV��v�&6�G�7���ɭ��`��4��-�ʀ��y�@jׄ/9	��k"���@-��n�����}x5����!n����H,��G���)���ޥ��H��H�(
n�����m?���⊖jK��"n�@���h�k}Q������-�J���W��0פ�mе�EO�s;KE��d`wkB��R\}���&<���xl�VUx /[T����dǮTR<���N�pE�1���Xw!6IB�))�[��Gz���pS"�SL�aw�$����o�#���&B�%1��A��'�`n�?�>�	��:u��6�T�nmGIf�*G��{��ǎN�������W�u�E���6[U&�y�zޔ�k�]<�&�L�����^%T��ӧ�}��]���7Vr��ˁ~n5y��9#7b<BW߮��������u�G��3�` 2I:U��ð����[">��]�x�\髠[����z�к����3�N;�z�	{�u���o۵�����Ӈ)܎��3��V�=G}��i$�r5�U	}��)0/m�}	$w�X�"Ffy�i��V�p�=�׉�ֶ��L�����O��w�.v�6��hS ���W�"s-cdoaZ�j�m3l�v�RT;�����"a�+ڤ��HWG%>Y�	��U���e�se՘�$��|t���J��~2"�=Q1F���J*�J`Wј���0:��պ�͒e�zh�&�Z�u�i�r�t��k�y��	φ}��^�f�a�>��Q���d��<g}g�x-M7�x�#'�|zz*�+��S�6���`q�MP��ڟ�.J������@	<��N]�
o���D�,J�0��Դ��bc�[��ΰ��Y�ۦ#�k����A�Ä�@0���oI6�ѬO����c���d��c`��W�ٍ��~x�V���`�T�b|h�z:��\���hd�Bg�j,*��<Rw���0��S؂mI����@����J��i�b!h`ԶW�	x�y	bOX��\H� 1O�L���3�*��7�ߚG���<q�Ү��Ԯ��-�4����Ng����Y��]8]��W8���!Bi��	���o��:���t2[v�C,	{����5U����Q0��!�u�G*� ��X��N�ƛ�����N�cP�����eU��|�K���13~�N,W��}`��~��2��J�<^���ɷ,�uN�X ��
�� 㥜��g�r�~&{KܿM}���W��ߏ�,�h��3vv�xY�Ŝ�v4��8A)~��ض���1��hw���M��_�#prYrÖlbid��`F��ֽ|F��(o�BI��rY��E%J�O�f�ث.g:�I~:`,�����0XH=�]���':����S�����;�՜�q�_��t\�H$�����e�tiyh�֦�v�����M
�O#S�&��m������6�[G|��Eȉ�䏏D�X�\Iʟjum����,��@&���:Eg��5j��X��KpJ������R�t��Yr�)˾����N5��ڬ�K��@��i���ʔ��"�8���Ł-4�4��w�S7��D?0�K��*�=,<�X��.�7���o`��]���C`�y�$4�*C�/�e'G@x��\�Vzq�u���*�2�o�*l�lJ(oc��[�<�s��ZM"u�(5!�!3��t�t�j-)G�;�G�p�U����$[Lq��*����	���e��O�qWGIݴFJ[Uf����$����uiJ�>��Oņ�B�`�2��L���!��e鏬p�J.��}o�F1�B�G0$�RWգ�r̟Ⱛ�� �Xq�Ә���r;��7�"Ƚ�4{��1�J}�n�c`��)�/����׻f���b�c/3Hw|������F�{$]�լN	fǪ��	:��!{::�{5�f�R�9�����I����-��r=�2	C�ث�g����F��,=Pmy�C�7:X��F�TM��eqt�pn=�x����~�(+�A�ϴ.��u�B�NoY��:��żv[/�����7�88�*33�q��aԢ��ѻ:bYd��9���WI�W~�x��^����c�i?�`�OW��ɼ�hU���k
�-�njM����&� �Z<�خ�<5��0�m%�7V~���@�эge��~�`WbZ��D�Y4�[�����+��l ��B,s5�옗� G���9�L��LF��u�2]�/�;�`�V���"9p#Շ�;�'�ц��"���Hw���Q�^	%��:�1��W�Sq�J���󨀛+�IQ# 
4���>����<����E�Y��VP��=�kb�W��hͨ}VS!�Bk4���t���е�؀n*�DH��QU#�^X�a͚�P���1	�� 歚+;;p�hT=�FP�#0S�}��C<�vBּCL����'��۟�_W~��4�h�9��q��uE�7c��1���Ur��nd���a�V��s����S�w�tMm���;
��x����4�*�(O�tГ�c����6��Pq�i�=�Ċ	���ݛ#11'7+ɯ����H��_6o󕲡wM�u��N�[���eUC�����;�?�O��`.Z�G*eԨ��U����%���vV�H���^�yS�f3{&@��:V)H(o�C\	B���R.�,.�ة�����U�jڭ'�����EG䗇������������9#Y=������/ʽ��L��H,<�o�%e��
�����n�}b�6B�p���úF�*�|�X���hm���e{�_�O��烊,����:ߺ�I��� i_3�0��D�_�Y��.�Mz��n���"��bƭQ�1u]{�]��I�~���öܔ�V���O�c��;���V��<ۘ�!O�|%�O%��yxjfȺv��j8Hh���g)q83�x޷���w�y4��*~qc���E���d��{<n� �2;�,4-�CD��@��S���~���A&�	;~�B�#N����Ω� �u^{�q+�z��bgt�FS�A��گ�/�g������F'�`� n�8���k�h�W����|������[+�����cH�t���ɟ)o�O7��J�{�+$��f�nW"�:X�*k��Gd�&p�ehF��-1
<7=�=:���b����X=k��A=,��:���j_Y�Pe���/A`����&����ڬ@c�;W�u�i�����dҳ}���cu��q��l�Q q����/I� �	����qyN1k��Ko�X�z�n͉&t;خk�9���ֹ���1_=�R-
��?D����۞���qg����������.��s�̟�3�,�=�+>�\'.g��A}��5o������*撵���jE�Jd��bخ���j��Vn�'ו�����*?��������&��\��yb.5l�"H�֟S��#.ِ��T����/�Ƴ�,uμ�O�_���R��:�5o4��u��&0�szĭ�=it�=yp�R��bz'�/�R��⎨g�,w�����F^<;�Q'� �#_K!0��w�$����bJ9R��/��㦩|�W<��h�C�H�x�'�����b:Su�8X,6�d���?�Œ�2ne28b�۝�X�7bkg#��� S�䰒�#�
�b��q��g������� G�2@m���~�VZ¢�����v�WGf��l̡���6y�ͬ�&��T��8CCm�t��I>�s�'����W��N��],D˻���#F7�`d龉�U�+�Z��,Ո���L˩�N�ܸO��es�X� 4�H@��*�{��rt��.ǅ�eC;j��7߈Ő�C���H�����U��	����ZA1�d���*~�s3첳�"�_t��pa �rԨEp���I/U�4���7H��v��[?��t�8X�[�{�J��
�,���;3i�kvr�y<�/�p��T������h&���A_+F�����kHQ*�r7�s�|`E��7��6�����.�,���0U�q"M�`Cό�$-���Wi���H	8���0�1�)mϜmt���VK�YA�8��K+z����E*�V+@.��]�!�'z��lC ��>Q��&����a�9pᏒ�u����+��-�-�"�cA���L���򰻜a;F7v�,��ܿZp���P���&���+AV�N��^
�W7t��-���۳R�.X����t��<�u0V�(أ=��/ўg&����N�Jy��؀%G���bL)�ֽ���J�y%��z��R���蝉��ط>��Z�	�Q#�ο�{]��E�->�=��P�W��]
S2��q�[�䪭����<3�X�F'� �6FM8�ˇ���$|�`�4��4D�t�o�;�O��~O)�ٍKz�߿ؤ�M��9^IRD����z�b��x���)	
�a�
P��a��Q�J9�#��0z�Җ�au/sH��P��������d���>/x��N�VsVyƅa`�S������jgt���Cꜹ��E?Yڀ��V}�IĈ�����<։���rˏ����/���+�ZV�M�<_\	i�w/:�G��aU�,�s�fN�?����`9��旛ZYpzS[U�Ҩ���X���L�(��_k�B��Y�)T
;����D5:Vs��yR
�K�Ź)���pc�ʮ���^ЗҴ�&�T���'GDs	�)�R�al���V��e�.6�OG�`�6W����h��՟��Sv��Y�Gb�Y	j	����'���K�Jf)��0���.���=o�8�y3��\��*Ά��}�R��
>���v�xAl��i��x�w:��?u�� n�>�t>a�u����jyǷn{��:� B�+�J�+���W�i?P�Q4*�+tJm}3\d0u���T@q-<H4>k9�tQ����:���jBj���
w��g"�Ln=6ݻ6�%b�u�ʰ:�k��$t��9���Us���0E,�o>�v�i���u�DT�����O��#�O��R͍kVR؟�7=g��l6q� ���n������%��"���+�=0c�-٣:��ǝ�}����(�����-W��//�%_��lĳ�C����)��E�����z �g{E	����U�%�\���g#���H	T�{�B���Tn+Yjq���rp��2���������AdB9-��˽�t*�W�a�lZ�0~S�xe����O�7ݥ Iw_��2�Zgܮ�C8�(n��s�d����DG+�4u��� Z
�8rSv�_�p&$?Q7%&%�~T��d
[/0#�Js�����h��c\5�WJ]��$�[��Ͻ�sڐ�2ՍU�ʫ4�I �u�ر]��5�f���`d�ԭ牢��y���ҋ���~�jhK8W��;��zsa`/Z�	��^߇_��J�����߯�,�ěA�˓�dHi���#�o7ί(�ڃ���T�?�⚺��x�ɉP�ػ�]�r��D���7XMd/ی5�כ�
�y��n�&[�~WY�9a��k��i����6���Z@����C!��U��rv�T4���tV�)��'_fޞ��~�A�:s��=u^�pϫ�Tn�_��|G��x2֗/o�L�|Du�f���R�,+Mz�����`���룺E8��l���7�Z�w`��U#C����-РL��#M8h.N�e���kK��^�u\LnN���VY�0�����
�'1D����j2�$j'	{J~ݐ��S���q�jQ���'�͛���;�_�×�R*��������]����V�Jgm���Ś�U\�!�����q-�rN�6ԿK�#�����>��h�9m�5��j�xn8a�t��Кma9>���V�*aL�k��	�F~'sO�T�(��[�'�`[�6���>�l�b�^{r��z�� N�.�0<s�w9��:���X�-�Q��U���sBV6�|n�>\��#(/Z��k,ZkL�Ǎ �_���DO+��]���˲g�VY�c�-�:W�,��dj]�}�C��WI+< ���!��|k���I�{�1 ����!�o�i.S�6(�3�����&���x邑���2�O�&��(he&w�+.�Q��a��h=��M���#g���"��{�/��Wĸۥ]S������< E��My�tBn&U�D����G�yl��D���UqJ(@��e
z�WpN��fl�����
���;�<>S	wn�"؛b�����Z�AS�=_`(c6H�Ү?�:RoEK�����$ǲ��Ek:wVoQ�~��4���l�����<Jp�fS�~�Q��7]��L��w�r��>��^����ʽ�g��|L���Dr��w+ӥ]��O�w3�Pc$�+z}<��BZ�1�N�xR; +:��'�m0�}1�o=F�K�Sl_��9Ͼ6��q�4OY;��^yA[7\�Ɂ_�vV�ޘ7Lײ�#�8�f���M[<�5Kj`����ɳ¿8��h�/���PR�o��J��k��|�m�Z��k�we�W7l�����ڲu��9B�>\��0p0��ي�a�&�?&ȷ�ٯ��a	������Ga$W_"= �'�#	H�"�+��6��ag�i���C���X3�4�xu!u���|�b���x���
֥�/υ��7QI�66�X_e}=õfi�8��r��]��b���q^��"6D��.ʧ����}�-��EBN�	�{)qN��Hi��<�N����v:=�G`\>��f7��e�
�D�;k��!Ƒ�_��$ߏ���׼y2����bU}(Tq�у�
FI��P�'������5��?㙙ʮ�G���3uچ��%�Ѕ��p3��OJ��9��N�D��@U(Y�w��G��O��PW�����H;)���/�Â��c�H)�D<D�n��Vc��7'���/��X�8��E��-�����r���ak:��Y�)�>�H��Xc}r$"5nW��#ϝ+���o��²��}/�{�|湥�k܌�Z��>��c�j�Ѳ��Ptaɲ?�z�j0��h�됩�n J�&���ʶT�+�˶��Hh�Tb�,,_��xC�^&Z� Z��Z�!�2K�ٻ���T�W|.2}f_WV��-�hMGM�M$��J�PtpNد��~��_�H��[1?�%$�ڟ!�"{���o��Li���g�'������֩_�!0T�Zq0�g�I��뽂L�Zn{��g��P������ЂNN�F���ݩ�E����/{���r-�~V�Քº�^��"�J��HdJSb��I��
��=D�"(E�fE?���
CH�)�)�bUL��.w��vV�t%cu��>�qn�0�OG��Y�n������X5����7�c2�����q��Urw��Ӊa>�o�;�û��'H��V*��ռ"r��}�Z�7=����?q�TU������gN�t�i�#�rӲ5����'FB?��|5iy��c5�`6�C?�"s//�T)�l�.��tz�r��d[(�/
��{^�=Y� ���ýL�/����t�p�~ݣ�i�M�x���-����1:ml1�G*ړܓ,u��R�x��1�U~�:�K���A�y�<��_Zܺ�k��1�Ź}�J��-�1���9
��uyX�u%9!v�I�X5L3I��J�}�y'҂�gu\R(v����`ڇ��BtN�r���\�%���B18̻kvЯ^�m6�R�?t1�Y��^}G$U��i�m����AS6U��v��	�G���(�%kH3̚�g��g���roH0+6�">�E��b�lJ��$`-i;���Kr�{/N�|J�Av�ei9��ʞ_�|���	[!=�Xd&O�b�!z'`7�aj�CL���[M�G_ų1<͓ݜ�r:��xpy�J~[����ƈZC�yz�5���F@��i���zD_{N�ό�X(?0G=�<԰~4@����\�h�[!�ްF6KYz���;J{/���%b�JD9m�h!갽bh�H2�c+�ӽ���61BMz�`�K����8��̬��b�zQCI_�)'|-�ٗ󮿙��x4,)��_��3
���2����@�ju�b0��عzYr��Sk+"��O:h�a� Gz�S�@��w�x,����]r�3ˣN�z��/;	�.^
ܦ���;�;�W-틋@��U�[.�`�8��a*G|��?�U=BQ\���E�]����r�>> 4��z�M���#� �������|�᥿��{��12�nog{��Q��|e�w�WV��QCt���0�%<G�|uD�-(䉓�K�� �
��鄩Į`���)d����(M�����v.��
5Z]e>	��B^����r��?[�Vw��L3���x�bH
*U��K�y��ʧm`��g+r��y��� G)r�g;���%Rqt�����??��./�v�W�ab�7���>�;��W��0�V�ĳl���>�r�����K�d	X}[�l�1d�}Eħz�s�����|�E݆:���^s*=�j�H<��j��S=�o�t�#�ͩ"	AՈ7���N�KB��)�=�爃X'5K0�=��X�VNU(ܐ�6h<B���!�;��"����� �n牭���=1�1'ze��ס�6c8�ʌ�\���^��6�gp�J�س�h�}��`+���B[��oS�����B�C/�!'�~��560��"��k��k����ok͵�n։c^3v8�S�ظ9>Â�����.xͬ�Ҏ����Z�w ���<B���	�FB� y8s_�02J�}�	_����z-��f{�wO�����1��*܌zK���3�R6��	���$Dd�K?x�PK�e��}  l�  PK  �@�U               word/media/image5.png̺up߲���!v��1����Qfff�$f�c��,��혙�d��$?g�:��ν{�[�V�����J3���FkV���� ��L���_�IK�����������#[Pi���rf����8^A��!�έPő�PbwG�w���ެ�#ZZ��͕fT v�!*>o�ݑ+�aɈ��"���IF�N=<N�+�Y��4�F�-)�w�F;�BW�D�n���mL�ڥI����s��hQM����`ѭ��A���`k�o��mt�AI�'�J~k8�{�����ApD ��|����8l������9��Fd�'PA~򻚈��)!X	��`;�֬��Z�z�*�����z$�������n[Z�9+��т���Q� �����h��m�%�8�[E¸��yrp��.��;�6���@�~�JWz���JQ�D]�H��v`Y��@7a_lr����8C��=��-[2�z"�8����m	�!SI�<(�4O�h	���j�V"�x=<��kĞюnBc������&*�rV~��H��䈅?v�b���މ���B8	��e�'?6iaR�69�T�e?5{�����F-x^�O��j���J� �5A���]KO�V�.���34�Sɓڈ&�vtt��"$#���~�,U/f��'��H%�v�Z<3{��֯]m>���\P�\�5�F!�Gڴ!�])Wc�qnH�o��v��PO�h�s|��J��%V��y^ۿn?1΄)X�? 
_B��PS����EC��@Q����C�H(>,����6޷��Ou��v����˵���#�P�������[Wz�__]`�W������������t��#xߜ�L<�k2Oz�X�T�2U�%���u�=�8~�X�Qg�R�[4��6�������IU*�L�-�zO�t�F��X�`$��A�ϵ�����[][{�v������yzGm��b�,-�t��~��>�}X� �\Y��i���o{0��G�_�����)־O#�I�k��e	�@��)`��D@��766���<%\��T#������#�+��� ����mW*�P��#������C�dVo�$đ%�K#��"�K�"))i ���/ay
����li컻���k8���'�lf��>��8"��mWy����V�~���>r���b)E�^޾Gޙ4&l��Bg6���)I�r|��R&�B^m�Ӽ+-��� �!�L�?t|�n��v�X��O.÷~�@�?/�V�x:�����U��9��3c]��2��|rrr��`h�M�"��  �&��ެ�Ak�H�Nn���sND1�W�ܪ����P��.;2pTh-|s�\*��#�Oz��v#Xw�:k/:��(V��q���	����Y�����3z����U�1�@'��לtW�Li�]����b�3��kr}�l������m3
���=������Oځ��[�n�^�ٴ��]��o[���80�����<^��/׽��s���K�l.��W�������Y�N�8���:� ��|cU�\�;bO�T�`Rk4|����S�WEs�_�
�'�`C_�'���tH������ ��~qk߉�t[�T�K�H!���>��;�[�:y�����<'KX����m��O�|�~p��F~�3�n,��z���a��p�lZ.J���{��/�\�{w�r�֞��mmma�h�k�m9n��X�E�I�B����n���G��W�	P�}�ߕ�{�ǀ��&u��ο�V�4B.�`Cb�'��զ8�l	�P`+��R��Y��We_5T��/��87X�m�GXA��j)�@w��a���f�0�m5�!�1{|�-�A�]����)>h2`>��[�2��<|ƈ��
Y�d�r��m����H%?~�y����{K���鸄�X�3�q���|Ǣ����Z"v�hwK�]s3���h�7�m�H�����D���
�6?��?�;ʣGl��M.��i�~hSCov�!��y�A���r�I���Y�	3*P���-�d�Tm��WY�S��u�-�Y������9�yi]�J-�t�b�v�Ӷ:>�c�x��_Hl��cO���5ue�m� ��������W��UR�.�wp����A�/3N���R�j�3�/�>o����U$v��ЂZ��F��TD��5�h��p��#�~���C,nX N��p���hF;���������ɞoYkW�ܖ�)��ThS��ׂ��-�y[��,���6�~>���]7����8���J_8�%uz���"��T�ƫ�[��#^i{�gQF��Á���k�����j1�ᄐ��>���8r���V
S�^�Q�O�2ٝ��$ʌ ��H �R�ȵ�aXV(ԽR���"'z�@{@j�9�ح¶t	G~��9��Gz�9f�B�jEc]�>�����?Q۟���J�|�R4/.��jt��=��:iH�����+Nt�k�k<�{��i�=��(Ty���93{�����w������ȫf���EX�iKm�`�g˧���0\T$�1�^k�Ζ*����2|	���Mͧį���y��T �����əӔ����8�������\g�Z���T�p},@g�W�$�[Zf�$(5h�	:|�������\���*g���DN+��=Р��������|T A5�5O��g!��- c�݆c�DYD�N�����eo =���Jz�iK,���&Y�2@c�A7�P��D�]��S�U'e�����"�(#5�:��E"�;k����N��)�
]�1�u����-��������4<4�0��eAK��V�{��J�]�14���E��~��H{rw*P�w�߾���B�곕(:�c�+�#
/JZ��څ�4���X�ZO��ض�.dS�{2�ʪ�&���c;-*<2�ԯ*��`�R�� '��-
��_ĺ�.��&��g.=��U���*�]P�|mMr<�b��$�MЇ(����)Ɗ���|���0�s#�����U^B��ZרY<'��t�&�a�0�b�"^[�c���	�ۓ�W1t�-1�(���F�k�ق|Y����,d�t��}f�L�k�+�KtBn���p����V�_Y�RE_�u&|��!����}JX��L�+p��b�h��I�.t1��:&U��
�~	����I�F_JW*{�^y1�%c��$ڴeT<˽��5l��<�t��Q��wg���ꌷ2��4�)��]ʴ	�t=�G�QÁɀl�����GJp����ug���5c~���I���}��Q����&���I�O�,L%n�[���6��4a���c��ԝ�J���#~�z� ������`����Hb�'���&◃���RV�Я[���sS�[������(i[����fA��WDN�����Q�H�.T�P>=e�缤��0��@��� �V��G�n�����2�rvSϖd,��8�=|�ݣ� �������Cr�i�����e���� ���p�MCP�VP�w��CDu��}z��`�
_�[w|O�Q���dz���-����zw�`oE�m�*`��������5�:����.�@�NR�5y[0ǮD��o_@U�d"(q���r����$�h��l���j�b�-�@���wcU@���$~�t����߂g��{4cEWY"-��m^o�����i�����0��T �{�O�A�ܛF��r51�~�z�i�Ϛ�YQ*Τ��fb�Fp%�	�'"��0X�����Fsq��8%2��m�N;A9�,��Q���
2�,8�0`_�&��.�ƸU���T3��2��S�Y�����_*4�ݹx �� �ǚ����'CP;z�7n�s�}�^��=Be&tZ�PKEp�!���E����`0h�����t*�<P�n��2�	��N��Ç�8�n��V�J|�/|��V�+�H�&D9�>�v��a�p�Zc5�~[�FV�|���Pr-��+<��� k�g��-x���z����/F�̷,���&�ovԮOZe`I�����B��5^?'^F�sL��~.�`ͦ��=�Q�o�E����=�.���_�\�w��5R�:6���)��[��p�D*��h�a��%�Y�/C$急�����:orE��PBH��-4~�-�;���e`��\�����~2�O�
��e�[�Ϫ3}^��_Ӫ���>��~�6���$�ı���^I����P�{�OQ��$�MKI�=0q���d����쵣�8�T�]^%7���I�I��z~KZV*��c�Ӏ�s�F�H�\N-A[}º�]�=Wl�i���,��!���i*ۍ��p�Uʺ.^�&F�U�?�����}:��g~���m\.�?�]��m�
�l@/�L9h���o=m�Rá�x���u��^��g��R���A���2� ����mޤ�~,ٜ��z@-U�v��F�����ڵwµ3���y����j�C��l������4��s\����V;���P	���D� ���6K'���$���Ns�Ӧ��`�U{'!�J� {���K��W����~q�ɬ��_2J����<�*�ٷ�]>��������'X_6#s\�'^�;Tx3�0rPA\v��C�kT;�բ>�X�5�����F�L��6�2�ˏ��V��;d�dKX1z#W�X�a6��>���F}��YK��p�<$�|Ah}�#S���T��CQ	�Y�B�ln�o}�Z���b�����jڷũ�����M���ַ݅_:��Sp��)�|P�n(�1swriZ&S�T�"�	�:������d��?-4�E�{1��{���mqК�ۜ�?��e%v,��WᆔO�v��r��d�*��b�����%='���i���:u%F�%�@	��$k��o,�^��w�ؗ�7:�����:V3�I�HP���U��p�[��ڇ8fa�L�b-e%���`s�'�A���=���>�Fc6����X��u��R�˕Z��k8��R��ʌB�`�!�Vj~|"�x���8�>o6�
��	6��Ցt��;0)/ywx@@�?F��G��J�<$/knaô�40�@�i��u�[Co�!�����'�U�}�}����I������h:�,ews�::��`���<��
�=��E�	�����}�L��Mv%�2����|�5{x�j>�	x#�Q�$�ԅKٜ��;}N���3Ƥ�d����M�h$�w����ד�� �a��'�Ү�MEIUgf'��vF��I%�n��w��(sU��W1^�/��[�d� ������O��M`H�t*���L�M�r��RQʺJ�Ɣ����b�w���QG�)Z��>N�"d���s[&*o9�?gIݻ
�R�4�!Ӝ�r�*���$�ٔj~J�ڪ�b�n��@jz��y�U�<��xN�$U*,����~�+u.;�hgd^�Zo�]a����C��Զ��7���]�Qg>u[����hy�n2��L�q6���-�J#�E��5�m�ϱC�j��p����D�ãW��媉O3��o�'F�I�Z��\9A�X|PR"�ޭ]���>lp�*��!'Y�����	�u��r?V���222"��/��%��deQ1�F&W	k���mˮ���Nǽ��E�S�����/����H�	�}z�?�|������D��'��h�C�#�wa�Ž�$��W��9��aQ5��n��Q�<�_� ���W�ӛ�X�7�^)����7?�7����1p��� �E���I��N��*_b��}��K��K#���eg�Y:A���T*��QC$G��&�ϧHH���y�K?3�4H�P��=y�m��s�~�//�᳷�׼Ͽ/ҩgZir��l�� �����I�<(���-x�'�z�Lo�C����F��ւ�$0�~\�?��&��|���I����	Hg|�>+A�%�FP�����������>�F(��r��z����a�;ok�S�qj*>+LW����|�5E��)�5T,F����J�92x�A_�> �Es��=�Cy�4�+ ���s4���l2!+af�ⶬ��Q����y���1�;���4B#��VM��y�aj��%np�'�8���lf��H���drUV�����[��"�y��k ��nxXd�Ş:�_ީ���ڊ%�o�����&��V������Ԇ�����43���̉7[�����=;��ͮ�LhT��@�7[pZz��WH���}�.&7����5�)to�����k���5O햭6��S�GE����ON�1�+p9�+J%�͎�gIfb޴��A?ܟ�׾�r��P��ж�1���� s[r4gg>��$��v{��b�鷇�@^Ix��O���'W̹�����-�K�{�t�l�:�L��I�v-���M���f��Lsy���T\��<�y]�+�X��� �������Bi�
!�J �H���wP����Ӏl[x<o�ݎW2��Ikٿ6�(ܛ'��xݖt�+3���F=[���R�wu癙��]P�3��Ů��D;�h��9y��:s���2N#g��լ���B=YD4�X4U]�1�j�L ���Q����*�����F)��i��rƘ�R�՘1�4c���/�Я�e5+>��+��?ֈg����,�'�x4��OV��͍wJ�DӃ{�fY8c)��}R
��%�vn_���i|��=�&����(�l]�0��e�&�O�=�uMdNa˚D$ٰ��y��s�|���9ɦ�v 
����܄�k)S�&Cw�"�_�)Ǩ�h��o�&��:*C��̜�����DL�
�V��&�#w���Y,��Dk��K8f��~��>��٫1�fs��pcc���"2�����-b �(f�n � {��i�s��V±1�
N�����s�H�Zk���+`���y���k�ր��e-��v�u��]��"#.���3^��y�/{o�fy��$K�Kp��{/�:u�����$A���)\�t=���w�n�/�dk*ega�I�d�����dd+$���o���y�3���-N����1@�H��ڕ�6ޱ�M���|���Bk=$�ɽ�o(v��1n0W�r5�p�e�S���wT6S���
Y�v��߁�g?��Y}�U-_���Z9	�*�k.���!�����͓�^:0<���Ҧ�%hՄ/QZs���w2e�_n���vV���}R�i�:�X~��q1��H�����l���<GV��۹i�-�	�џx�*lU�j��~�*ɖ@R+�v���&��gL_���d԰����2-�â��%?R2^b��"гp���hcgX��K���m21�Cvˁk^��1&	�N�d��Ko<�~�Zk���&; Ҝ�P3u��������%��9��tN���a~���ߑ�?X0rF#��Þ�u�m\��J�BS�����:=�s���*�Z����5v%������)($���*�0�H�I�(��?sĻ��f��͛xW4-ӎ�`;�j┍K_�s�I�ʲ����m߇P��j걲�D�>z���k���il�_H��y��l}��]��q����5g����?�cTI�u!\c��R�<z]�8kt�]TO�O�H$��/Aί	���#1�����N�,�s�o�I;�Z�X�.e���_h:$?N�ﱂ��ܢ��w��T���z��,�>1R�yh+X��~<y�J��Xy��/����)�������~|��������>���H\8�J��J��2��Qekr׆O�x0#z�򠏘��7�7
�®@�KU����M�2��b�w����C��;6�~0�!׫�^B11�ƒV�C�i�9C�����z�ҷ�S>�=�P��R�Z��������_�RE&�Lc���0�Ԉ�������k4Ȓ9�O=�Z�;�A���H��x�}���:��	���mN��K_FJ�x_;k��^ek��Ӭ�1�?�%~���I0�����[2��}D��L�ðy?��Q1�1=�4g��j��i��)��G�;�?6L�	8�t�>eCM�H�`�	�,q�n�Y��ɷ�K*qu�Hbg�;���jʰ�c��7R?mg��У�ÄuޑJ��$��u!��q2m"��Tݦ�T���!�# �RF�;���GM廇|NW�g{�C��xu�-�9�|��u��%�ƿ�T�
�w�
k�&���ƹ�=�L��2�s=��v��r����~�7����U�������^��r��:�i�	1������jv2�ㄵ�޾6뇺�ʹ�is2�6�F��Eu���y�/����XQ�k*O�F��+�hjPm?����#km�Jr��v��&�f�pXHX�� ByÑgy��>�1A���E��IZ��Y�J������<���/���S�G@��@ė� �P������J�kr���3��g���{���D������e1�U�V����>���6��]p�gT=f^��z��U�@��T(��0N	G���?�L�Zse0�?����� ;e��B�g�i�4P�7g�G����g_��Wﺡ{z0e��P`}��!W���$[Q�숵������'q⛻b@��̲i5���*�Vm�(��h!h/�sD�u �a�2]�n͒��l�X��#Цp�f�͉�j�68[@���9Bx�y��~1�4DVd��}��Zt�\D��F�ٟ���6�q���KԵ�K5G��wJ4��ʀ��C�,��P���Qp�@�>�Y;��/Y�h�fɅ��	���v����3٢%a^h��#ޞ�T��dR\���S���_]w���/��t�'N�$���u37��ʎ�#5\��BMu� ���jif�~����q�r���]C�z�P���̭�U*�?�x�������s�&؊ݍ`��,y�����5d�N��Ra��J�X�Ũ�QZud�\g�Ɲ��_��IyMC�I�i|�W�����B�G-�G�{��Vk�IO��/�ٱ��pF(����W~�)���0���4�B�qT�!��7��p�Ш�B����rd��y�DQhH�j�,��T/xr��S��']]�c�~_�{�,�f02�"ٍ�Ő����g�J�C�ilX|.(��T�Hr�m��;�GY~Ū�>��w6��/���9�O(�|5r���I�}ލ��fY�wX����dW�����0ه����GW�S�xO���`~�4���:ڏT�r�1l{���m�v	���G�H��O�ജ-@"MSjr�F�r��#��v#�	l#��j�y1�d��3J�H3���#���� �����7��4�j��s��0�EM:?gV�C��1S��A��~��ֲ/���EIۿ�I@s��4�V�=Z\�'n
o�
��ܙ�Gk�l"��c�%zZ]Ջ��*k:%`�e�XxB+�!�6�|���S��0�AL৕�\��]�c�-|�>VT���̀NN���Dg���u!���쐞��,�SzfZ���o��^�B��c��t#��~4'��\�7�u_Wߠ���`9L�Dj�32V-����2������?e�1Y0�͍DTCc��]-k�#��f;�-�Ic����9������Bԉz3�ilb����g�H������k'�)8�$�X��a����GG�83dh�Ԭh�ASB�]��t�;3v�^�&��Y���r��@�����-A�1)��@#��=���B�z/��Z�r�T�X0���ݟH5v��|��
�&���7T&��K�<�RG󎖸ZU��vU��r��|� ��@B��
���S$*�W}�h��J����>�� 2E��Y�=����c=�{�2 h�������zVk�1�P��9֘��
E��+��e���6��V��Ig�_���D�)�r�:n�a�\��y�V�޲�ڹ��а7��Q`a|d����;��@j1�ҍI�h�q�U3�~�k��ijGܚ]��+��D�%��a�D�}�[�&*���Q5�p�.mx_���N�wy�&v��H "�=Īki��zu��˞=ut����`����rv<u\����3O���R'���s�]��f�}��7�Y��AЋ��ؼLEa��+��*���jC��.���������Q��@�:U6s珡�����.U�wsH&E��'����i�k�\#�5� at����W���ዝOy��䝁��ײ�MY��7��i�<C�Z<���?9���K*��;F���sZMz��4��Ƨ�of+�����ŞC<�2��Y�>��K݁/���2���~��3A{��뜹(���:j�cm����D��GS��?3nP�n��m�<���C�o�q{A��B=�5z55
u���k����hR��������RG�~�Ǌ�e�|�RE�n/��i?W��&0}s�O0��Zf�u��9܁�K���6�ڵT�k��}o��0�Ջ���涧���P)���Tf[:2�7�����Q=���\��嘫˕���lc��iz�
�70�\
�Jp�!,ᕚ��b�����a��B�G �f��IlS��2��,��2 �j�|¸H�/QcDַ�L-�hqك�w��0��,�J$�����߲�zEo߾-pE�㳷��#0t!�%�%H��*�%}�p�N!�y��~�D�:��R��VT��g�?����~x$\�-[��ќDr��� +�y�A��T���$��2�Ý ��&�Hb]�d.9ڧ�|�Ȫ�� �(L�CYd!�BJ��~��^\�������*�\���\ɦ���'0���n���B�[��t4Ti�K�?Ϭ�k--ږօ��eR��}Ak�ۉ[{�,��)�L����<� 镅��F��i��X�=>)5�}��r��[�z°�h�M�$hhfu�{[4�1���t����G,�D��wV-v��q��2Z5�F��-�a��S������y;��r�g"�Zt��n�\��7�W����u���� ���%|�#����|��N�:��1�j�i2��j��>H�>/�k��"��+rCz_�s��{G�������Q���\�9���pUy��I{�px`s~Y�b���;oCQg�}�"6���+bl"����ф�h���U��d�w�������i]s^Ʃ�ށԬM.n����d�6~}:�k��-�h��F5�@�,D����J�(;tqg�m0���'4���Z �f�/:�bދ�=4��XI?�R�[��M<���{u�vk�/i��5�B����(;��d��(]DxB��ar�F�M�'I%i�����U��H�{y:5V����m�x��w���T]����'���b��JC�H�w5�$�~��Tz�}��@S���,�F��s�b/d|7�3��R#P��pz��̦އ\���ڇ)H����L�~)s�<!1[Ha�̌�jgi�`ϕ �:����|�w��zwg*k�Ӫ��må�?K�>,7����J��GF�P�>�&g+��$Cx���yr��R����2��NduŜ�Q���2�}}Do��7~���f"���0�gpel@M�6�J���@�!�j��姦��T��ND�L3{�~M��>�2B��苈�F9���{@Bx0F"�Eq_���u���7t1�yk&�y��Yn��?V�$�u[J��	�V8�,S��(&�LLʃ��+M���W�����]��d�����8Y��?ʕ�"��K�9i7#N&ܓJ�]�ˋ����B&�=D�N`ɋh�JEʊ��#cw��-�n��Lw��O�Ù
����`'�n��C;7�OK"�&�Y��D�I��gQ�LA�C��>c�	�}����묓�h�w��G��<� o�<�%�	�Ŕ�i�����XA��!�������r��ߗJ?c�3Y���_c���� v�l�2%5���[��wGܜ���Ao��Dz,����z]9����ј�yWI)�4L��ô��&���M퀗�î��>��P�����~�6������T�83�Z���z.Z3v;�F��7p�g~�X�g�iKt�T�T���0d6ٖ�K�V�i���b�ZSo���dSP����&��{PX�MzI����z|H	o56�����c.�%��Ҹ��b#��ѥh�Br�pZ����u:*�#£�1��}4�o��e M�i��
�54:����7%*=#/3����iz�4 bLQk�-����\��-��u���k6a�YM���.g9X�Zz��"l���}*IS�(�0���k�'�1Lp`��:�O�	�:�hu�a�0��-%��h��#�<�7���ϖ�'�_�V�1n�M�^E��M�©��8�f���~C�~�f��߁����E�"����׍��n)�@ڙ#N�;�d�QߴD��|;�S�����r)}I�:$�p�a�*��3Rg�m�KU? �/�&�J<�enu�2�q��F���)9�ѢM�~���d]��b�Q��ӹ�c�֨0�D��� )�������V�]�kC�[��Z>qk��z����FR����������>�0ZۋC�����'�񴺾yw1����Z<y��J�Ca§ڹIx��7�U��l�á߂E�P���n�1�4ao�ѫ�`�%c���s|�Ŭ[6����~g��������ٟB�	�a}��e���\C�AjQ���d��G.��X�"�ڜ\wF��j�ӕ+[A����>��_�3B���b�:؇��WV��"�Sh�<g�`^���&~i��Ls�)t-Չ�Gӏ�O%'�ӦiEә����]TZ��T�(-�o���a\h�ذ����Nӭf �����X��{�s 2��x)�w֐LRg@��Sqպ.�
�b��:-X���F9�EZ\��|���-�'��}�$�W�����<�92}澕>Z59G��pb��I�#�N6�܉<�������8$F���ޱ�|(GU8���r;�_�>M5����8�Vf7'ϖl�PVw�ڠ!�����w0� i׀�*����~{�j�&��ˠ�8�(�� �5�BX3}�O�!ov�.n;X�A|u1ytT�8���D� ��{�E��]��̛gJ�j/�8 -��3�.Y:�W]�g"�B&/�+�'
m���O�~��I7����v��p���+5��e�#UM�̹peX;)>9$�=`�V�yZ��Ddߵ-�K
�L	3Ѭ	1I���q���P/Uyk���Ե`��-�vy��O��F��\�!���Id*6ߗ���'|�	��E��[a�����W�d�R� ̧/�f@u�*�%�|���t�MJ$�n��#�?@� �&�>A�ȅ8AǪ?��!�>�y�0ܢR�O`�Ȕ.��ir?N��B����@DB������͉2[��:��o~X첾n:�@5��ZJ�yHQ�f"W�B�,B���z;�8H�wz6�<)�b#�\JA3'8ߗgߚr�d�oF':ݰ����0�q���;��*�;g���I�Ǜ�y������B�� �M	���B�!�y�7s�o��1�Մo`�@F�c�jXϩԃ1OOsC�L�$S�Z�X��6���Rd;�v[�����>��d����B�
���pB3KƷ��*	����<�DR�yI������ۓ$�`���I�k��Q�Rç��ن�Y����AoE~MA�O0C�����52��*Y��A�xr����+��Q�Y��&��D�P��]���!���7�SmW�~\�mY�����m�G��=���*{���{��mb!b�BWUK�~�_�uXTԞ[�+�����5��nyk@t{�mJП;�J�*����*d��4�].��{"�X��ŏo�X��_z;��y?L�ux�����d��D��Rֈq���uqe��3Q-�$�u�Z�^�HK��&I,�%p:d6��$=�wS{�G"6�.��ʾu_�x/�UyK�o�N���Ֆ��|d{W,���p)�>ݼ���$[�S�7�y��F�&#	�^_p?�(ca�BШ3���yz8�S�EF��p�a��&3y6Y�c�ϵ�o��_\�Y;Nb�<eV;9B������3�e��Τ�2)���N	KH�U�yĲ�5v��K"��Ų�oP��I�� ����{�q��B0E������Bj��'S���4�Wc��a_�Dm@P�oA� ��n�%�(�O�j�?Z����|w�-
Ah���jE���D��9Rv��z����[`�m]����ߓ�\�wK���5��RsS�Q�wcI�����u�m�L���m��3v9��0���*s�����ک���ِ�,ǳs��u���K �45n���7�ԃ���올TV�Aۚ�T�ƿl���׎�1V#��L�Ԏ�Wl��d#G�!JUߌ=gc�&�ml�w�Ψ�y��z+��/��2��l����R�B�k��V7@�(��F�	�:��7�1��kS�����0���H��E*,?��v�(����u� ���?�w"*�}[FL:��tR�T�YK��yI����^,p�QP���#V��� 7N�vX&'���5E������u}����X�K~���t<�	�;0�Ɇ8��C1Jބ��p�As"�͔��8?��M�n>��9M��>���Pz2�=��Hz���;
Y-�-�FaS�U��7��ɶ�?�}�-Fd�	�9��g�d�8����L�W���!�V�}�{���*`3��_Z�Ԟ�\�x51����U�p�;J�9�u�{{���$��8�Pe:k�v� ��W���Q��k�e���j�i���#�Q�������+�Ųli�|E�F�a��T��!��uF:��g��0���<J�G��S�p
���iEo����9��|���!m�h=YV��}���E>���(���qkj\�1�qO�õ�~?�{ّl� 
A�	�_�ߚ�RUrN�j��-�P}�L.����!�b@?��Ĝ��l������#���̣-h'�\�P�ۜъ�D�l�v�j>�φ�sۘ'�ZU��I�M7�I"c��ͷ9i��Ī� �*!�+=Z�j5�=�"v���ͨL�â��J��K�P+��%�ǅ�2�#���x��X"^eg	&�A�g���-p�w��;��ّ'g��I�S�J~D�.	��t^���]�7��]X�a���Z�᪟#�=S�}��ea$F$[�R�o ]#�k�C��{	x�Kq��Z7���=qQ�Y�T)���m�R��y�E@e�����=��@ltUI(�M�Su��#�<V�-�2���-����?���G�\aR�3�r��]���LqAܟ9	�c��θ]�&�0A�� �3['�t�h�7x�����$�&,MP�V�oەT��#�Y˵\a���M���k����u��@�
}�n<WQ=*fYX#�����G>9�m����FA�ZG���CPEaG�� �x�;���;�Ww-M[X�W���E��z�k���ҷ.�p��z�,v#��~�Io��86��_��QEV�j��슠�0J%������\����*���<Z !��IBK��R���(t�V�V��K"'�:���Y�����Oov�E�b�^��Sz�y ��'�:�Uё�@��0�v*��@|?�M��'G�%�|�ٲ瓑�!�?KnZv�:�3/�i�FεEl�/\��;h����?���a�(�f��O�5N	�u?�����3I*a��ɐ\H�����ތ���wӗ0�%�sE��>�~��������sm���4��[KJ"l_�����o��-߽���(ڨv-�~K��*B�)�-�V�I�Ğ4l�&�*�[�4Ȑ�?�V��\v��f֐v��/[g2�8����\�WT��r�X�Q��R9zFT���0���ՙ~/�.Lq�$�I��v�B
F�� Q�O[(hs����U^K��@���.��o�t��0�^х�L	�lAZ��[��rD�Ns$ݫ�P��x���.����l��2k<(���b�v�R<kЊ?'Ĺw�$S��09C�3�	�y���1�U`�m���
��7���NMx�
ul]1y��Y(R�����n8�Bf
^�T�WFP�<B=
��2�4	�<��צ�k�eY��'�n��t�֊�N�X�	m�V���Zֿ�L.�3�`t��a��R�e�ˋg��C�m�T����oy1��o��͕<p��?	7b	PRU��yXf�r*+���L��h |Ð����@����AnP_n%TH���U�X�Z�Q Q�se��g6t�]�/P`�6wz�ق��w�щd����0W������)�����x�礛S�-	s�e���,�{�^v�{���H�->r
C/���tk,���e$��?����k
�1HVlQH�"�{AY�^m�A`ik=	ְ�]��'��n��(B>m�����L��_��N@i��9��M���������)�i7�-�����?Q�,E���|�u��'$��só}��QB2՚�A��GK NnZo9U�Փ�������t����!�2�Ļ?Q����ѝ��[�d¨or5^��sN?����kT�͉.rWFV�3����@Y=�H3�ӄ���&����y���}� <?1nS�co�$S �ζA���'s?��*k���"��x+���!G��p�5�Hs�L����_/�⣀�O5_�ڶ�E�A�%�s��A@�f@������U������t?��~���x����X�f��^�^�u�u�K5� �Ơ�b�˖�X���?�=��R��S?mMU��R�\��{�W��PZ�Yyi����<4kV3���7PX����4����K�s ��%�_:%}�?j� X�~��z;5��J_�� ��s=�f�V_��jD��?8Ӄ���A��Vm*�Y�+���y?�r�`cE8�F��gF��.J8c��l�����V��cr�~ߋ����!�>@�X_�夼j�J���C>���`����"^`-��}�P�9�թDز<�@u�`����լ}��O����cփ����Q��-����E̷���;>�������ԛ�7�_�HΒ
q���h��^Cr��Hh�Y��L�SY��������q
S��Q�B�������;�����B���[h��kj������B)J��4C.���/�j�s�Ԫ�k�X-%�����'6N8~��ɗ�5�9񛘄!m���@�	�ֆ�'���A�u��#@������\l���F���,^}�T��}>n�<M��~�v�l�I^h��&���yȳŐ륖a�@tJ��$����MߪVCU����:���F����|nKTe}t�����bS�x�re���n�lJD�gHm�#�0���y�k�^�r-'�8X���Z���`�ֻ�tPѯ)_`�z��T7�9sc2�D��r����D/�G���-�J��!>�"֜\�Sd�Ց�\�����p��]=���lF��2�&���w���N����4a!����8bGe4�r|l�e��7��{v�@졺z��fa��k1�l	��ˋ��9Fڭ�!�!���A���[�\d�%ӌ�b�6�g���o�.�mR!��4�n��/C�����%��O�3�E�w������2+��x:�#�v	Y<���F�z����ֹ���דt��)D��:G��@�Yd����s�d6Q**>�1�n����G�N�=�t8f�c��tx�K�;}x�����'�@g�}�G>��������+!�s��
��)��T:g2�����'��쓁�tP��Jn��G,�Z�����Csq�����V�Ƚi:\$��0�����֒ᜯ���Ͽ|�)�=oȖ�k5�����YO�*��%��![�d�hs@�iۂ��sY��J�v�q;�$�,@4,?W3�&I&MO<����!��Y�k�+9��'�ː#;#���O簐/@�O�8��]:#����v29�P����H����&�b�\�d?�ef㍢����VG6e��񶙀�_ܿb�m��7uN���e!D��q�/v�;�'�~�rM����!�MdI�i�e��c��V���^��z�!z>đ �FFͽ}pѿ[	�)��>s��f��:��dM�3�9��a���fx>J�׸�,$��M����|ɶC��ٜ�7�B��X(�]�} @��rp�������a��a�k4�Dl�'���|_W��Gd���xF߰��Ƅv� e���i(x�^�����*Yg�3�j�V�@9&�"�
,ףŝ�Sv�ֈ$>��'�8@�#%cs��S��B�th��4t��b�Ơ�u|�>�q��Fp�����G1�%�����IDR[�EB�~i��;�S��,&�f�6��:�>��L�N���T���B������������3B���2�Q�!6�cj��ƃ��J]E�n]׃F�~�Iڣ3��
{��
�m���2�����5ɍqhuu�����S5&p+r�Ъ
��7�t�j��p*Y��C1��8��k���C����s�h����t)�{���"VQc�P��/����S?����UHDgD��:j���<K
�"��)rC1��PLhOQ�a��{mM@"\!���>L[g���|��q�"u��ay<��x���c���m�+���Ap�M\x����0?gFQ7�\��+��d��x.�I�Wϡ���)�o�wW^d�[@�4���� 0nY�$^��3z�l��u�b������?4�xv��J��lkd�t�z�4���G��9�y<�'�[�:���g�t^j�z}R_a� ������Uc=�V<-O򻱾�&�;H],�LRJI�$!H(�8#7>�X����M)�� D��f�������muvZ�|���"�Ĩ|Vk���X�bh�I=�H:����f,A��i0mg�uL�3�֔�q�ψM�=�4!��
�}�B�����0�w�پf��W�ҁ���@�&v�������h&:������˅t��|���7�Ia��~c��&Mg��N�����<����5DM|aI�ӥ��h���`wF^q]��s����~zK�|���*�P�(�'3���d2��T����y��~�*�v6�]-?F���3:smj�K�2��e��R̝���Uݕd6+vE��\L))����v�,(��m�K����NZ��Y�d�Q����= L�4۞��a{偓�D��`s��,[7웪�[���@.��R�a�����ہ�J2U1�%���RqMlK���f���/Dn��<fS1��Ռ.�ؾ�m�#]��!�U�w�j0��T92τ4b9��ك�y
�Sm	�rBu�NN���A��!�F�B���Y�8���>s�+�=m�N��OF�(l�z?���ju�X-LU�)�_�j
��"����o4�����^FR�f�R�V�L��%X�*�U����ν��XU��Y�
��r����mf]
	l&>�8/�Y��s�j��x��������$�P��I������~в�M�j���խ��<�n.����l�[��������FF�'��N�
�i��5����G���؉��������������خW�����~�5S���hNG�_����>6����HR�ʤϮ����h�5#��DT=�#�޶"�y7��I-�sE���������u����Ҍ<����AVwx�I?]��-�m|��JK-S�-�S�ۅXHbͥ�k�tF�F�b�
QK�]�I��v��w��M�.�![�뷮��A�m� cg��sC%����o(,Mݡk���d6�3W����lZ���(~��[;�D��fُr���&�z�+�yZn�E����$�yɴ,?ޏ}����	���zk��x�	�֏�����J/M�����q��uo*���.�{��W)wG,��f����yQY��B۫�	��?)W�V���d���0N��4?���V\{��,�>��s0yҒ~<B|m/�`v!�R[�Y}��T�opu�\�Ya���� rJko�P���?�Q���0���\6���؏086��}MY���1U�_�FUT��� �٦�?�ZS�iQ��*��"�D��b�#��n4+�l^l��J��Q#��t���4������
��JP��M�վ�3r�L��������0{�.��D�=	r��A+V�E����މ�?=a�)W6�%טx��r�â$��_��|;	]ݨC�f��s��{�:���P��P-b�A����-�~O@����~S���2fcΣ��˴$��y���g���������N����>@^�.�޺{��������zCQ���W ��g�� ��p�~��EGFJ��{=�P7�s|D�f�-�^�u�`GO�i�����E!|�4�/Mh0��^�c	Y:y�'��ҞFx��������,<)��	��^D�@;,G�L0��g�l�wx�ȼ`#��9���`�s�<(q����y7�ŷ�Nm�K�S��^�xh�j�׳ӹ�tt~�i����Mܞs[��&	��c«3��ҍ/H�AZ�֍�4�;�8'��^��z_���c�%�� qp�Ik�VR{�Q�R=a���W��'g󕗀e��t����?H�y�+y��_5�LB�����5j��ǀb;F��-��?�k}�6%�( l��η�w���P����� ����|K[ޱ':)�N9���%�H����ms��[����a���Q��oߢ.[��t�(��X*�|	�������?����y{�I5�6��,��oG{/��lK������~uE`U�#�B�����K{�ߴ������ܦ��%Mɘ5���nh���cj�Z,ނ��&�	�_�����kӈ����d��}��Ay�A�b���k)�T~u}<�V��i�meP)��P�����^��nh%���.��̉��a��]��K7�����e����(��L��U�X����5S����;�F"��M���\c��ia3��܁�Ǘ�W�#E�9'�$��̃A;kD�"�̐V���Y�gT��҄jT�Z�NG%R*�ߤM'd�_�p��!��u�	AFހ��t:h�c��q8�� <H�Q����M]�tϦ�P�tV�MeF3��:����D�"ta�T�cG�m$̜���h�������Kk�v�}f7l���$ג��Wi8�2;\V�w���N����k�	���K- �����'��ݏh��h�k>5^�c<9F�~�5K��V�M>>�՝s��9��s�.��H]u5F��i~�A�?;���bHh�{I��̨�Ij ���~_3��Vw��0`��Xr��7��џQ�j�6�y}z/�B���Qw�V>l�,��X�1��js��=���2��C�R�R[��*Y���������0��"����P.�f���D�*5"����a>�$���攒���LHk#��A������ba1����2��sׅ�_% 1[X�v�="����`�0t�F1Eu���׺J�5�����a,�m��dPEL�g_�KSX�k����P%�a��F:_��}��	[~�m5��%�t��ד�j�iz�w������k�l��2�	��%V�?V�鿐�#���6匾/�@kyl1�o�j�i�l�s�'2u�ret�pĮz[�rN����<���V,�h˶�ڎ�C|`'+i���A������
� �/�6]��}�ʷg�Y	^R֑�����#a+�gW�����㐍v�kxqJ<�G�Xͺ��G�M۬����~��Ջ�@yC��g��Z,��m1<�q4'��?���_*n�<@*R%�n�>M�V�mA)_=ϫ�\��^%�`!k�'ew?��d(�	�g�.���R�k��������D�����qu�ֽ�8I^�s� �e��C��#5v��*�N���F0_B*�����o�e"����X�-|0;��� 'ø�)A�W�۽P) �[W+�	��&��e��L'fw#�l���]��ʱEQ�s�8�C�|9i�J�I��"E|&j��Q^f��g ;$����H]iɽ{�eá�M���뼠��->�g.��)�딛uǥv���I*kIJ�x��4�=����k�'/����IJv��s~N�90Q��5�>���pw�M��|����=y�
�J���*���]�ʯSsM����C�@�*Xx�X�RW�(�������H(�B��$�j��X�_��6R���ϸ��C�Ҥ�"F���N]=H��l��p7�e�z����c@?d�ف��qz6�!�1DI��5�)x����k݆֡��k}�0�౷�U ^�?1���蓦p*UO�v��蕊��V{sXB�|ڑ<���i�=��0�;����$���n���¦��N���k���g�n6���Sşz���t��K��:�f�Li�y���(\��<����X���6E�3������wy�7����r��FjO��J� ��Bth�%ڶd̃G�/�y�'V&�qf�/+Lma&����UWZŒ��|#I�D�_P�஥�U�"�ceq�0j����!ɐ��iN���ӄj��I���+�oqy_V[e�o�2|u���%|A��\�&���.�Հ����{ҝ�&�Q��K�'�/n�Z�_G�U���I���G+�Yl�&u�[$Q7�=�Lg�>(���b����X�68^y�O��������"���4Kg0!W>E���ed�H)|�����4�Kg!5�n�"w�VRg�dvJSh���C,�w���-~��L��0����x�H*Su��1ﯴ�cW��;��&ѱ��;j:6���S�-!n(��_7d���O.����Q����q��:$I܉�4;�8jy��\m�3W[���#�ٝ��ofu��ܪ~�CR���Żr�^GyN�^�i ����R2TF{�7s��1��g�-�
�cc�*o�����b�c2!)�NSp���x['렵�����Y��F/h�b׏�춑�D+�1�H���ϐ]��Nu�~���NA�ˀ����!ү�[�����s�D�4�F5����a��첇w~n��e�m�c�gqQΗlS� U���Y��hE�Gc�=t��<��miΟ�]����ѫ�e��tI�v�ˁ�>�?��oIΥ�9���M�{g/Yh�F�`��uWu���˷��ԕJ�
n��{?WKzb>�ǲ��Ěu1V4
�_2����R��Nf���+��F�4�
�hT��O�̊��-���?�o%�V�s}���')w:)v�p�QI���S�LL  ���Fg$+��ò؂Y>y�|5���w�!p���7��>$Z�L��#���꨻�o"e@�C�B��N:O������a|������0���z���T{DO7;)I*6_��q�_�<�'��̟\��o��?0ԑc�LsOT�we�j^"�h�Rݥ�����ΑJ���'(./f����,prQm���K����_vzS<�!�������w���"[c��S@i7ձS���]��Ds���T�l��Z?͞�;�ψl�����Z
����B���)����.{wI���	��A�3�R�C�Y�����	ԲUZ��াJw&���/������~B��Ƃ�DT���KCe���H�9��E��$S.��Z���L�t��Y���L^�̦����ί��:D<ҧ:鼲��2+�.�Nj���=��k�˃��b������dg�< �&�sW��ܦ5�B�W!�\�Pـ5�_t�'а*����;s��\9KH��<l=;+oQ񂉇3&��S�U
�V1�8(��Hd*WD�����3�o��������H-?�WL�
��(�!�	3�&�Hp����*���̦�]|����o`ę��!�K�L;�K]�j�U�=���vj0mw� ����@���M�����Y���N
j�K8w>�\C��2�MO������A�$�L�9�08A��C|�|%�5p4�d�=�� ���P��}�E-�*��I~�:�ޑ���K�8�����0��8��(���O0=D������g- �RQs@7�x�c_@�h�I'��������y*�8��E#�"��-4��A:f��O�7S��&]$�'���R��'���{�/R����!���x�r�Nn�H���#�W��x�o��6���|���� �4VA<�q��K��&�ߵ(�\�8ǘX�Z<��{�_:��ʥ���J�k��s�����C��Ϧ\tL�u�jff��M���nH`֚�-E`�V$��JRXG��&a��s�{>Mٹ��6+T,,�U&��V�J
��(�?�G��tr"�{�$���ĳ�{��Gr�D#{�x6 �3Q!���y��6Z�ђrB�ߡ�~�MV>�0d����T����g�/�/�Ɩ���L�Fp�A��Z]5(V����k�,D&OoXTd���Y����bE����� ï��?���WX�g�Q��A#�ayXh �W�k1+E�i��3��4�q����d�q�������Sjmy��^pQ=�WO:�YHp�ߚh&[�+V���BÃ�Ӳ���z�v���k�Ӹh
�Q��|{z�~G,J�0
�n��o����c󑩑v�o�[��aw)w�op�ș��󝁆��_I�+�;Ż���l�XK�Q����ì��|� ���0ʇQ�Nb�FvB���i���<��T{md�O�]Z�x����[|H�Vt���^A�]`��`�p�=*��{��>�~V)8�i��X��2+)����7������(�*�~ isܼ7��� d���>�^4��b���䯏�6��g9W��>�!^��L
5���B��|:,p�f��D�"KN� ����\iϾ�qX�/��94���n�A=�蓦w�W��3��p��Sm�4��%����Db��g�m�3��f�x���b�#�:r�w0�<�-}�'_}��p,�1��v�����TU����:�at]_�3~o	S}x��,?�3�C� ��s��h�W&����#l;�>��*~���]\U�E$<
~c�6��/��9�هu��i��{�9��`�C�6y
~�B6��͆.�߳��~��qa��
�q}w�(�zx�.����rA/�U!�ێi5�p��5t	~�0^܊�q^����A,��=,�'����*���p�)�����7�(!!�X��л���&�?����@���E�9�+{ыrV�n�'�|��d��M�=e�N�-Qx{��J� �S��J4�S��'�x$�D�Y�7SO�䣺��w�6���p� ���Je��f}Hri�g.W+�i�2�,���96�z��u+lL�|����J�C8S,��_χT:�x��+�I���]��D��`/O�E
�z���:%,�)��Ȳ+�F�C'%~���[D��n49xӉ�ܗ��eƾLg2:~n����D��҇I"u:�U�# �ER�5v�e�y�9��/#�`�+Iz=������e]�M����
r��ć)�n"D|Hm{1��0��@��O��;Y8O�W1/$Wb/VʯOz!�Bv]6>pX�0�0�|Cr���`f��*�P-�TI��5^V�;���C#0_��B�/��G[.Ξ��`�	����;Ҋ��@����v܁77���x`�!0�}�䌐O�ګ���'G��q�1��|�i��O6��lu�n�5�Q�q��AX�x,jp�<��/�#�חV�po`�\H�if��`x�S���:4!���1&�j�\���
�˃�]0���<Z���*���B6ba�돨���<���� PKW��Y�e  er  PK  �@�U               word/styles.xml�TaO�0��_�{I[UUĂ�P7��si<۳���g;q�T�n_��]�|��˝_�K=��T��N�(NDF�2A�7�3i�y�����hty��|5�f�@G6���*A�1rǚPb}"$p˅*��G��WBeR	Z��%����i\b�Q(3�t
��(�EnN�(c�甀/e�GC�T�P�$�4Rb�TɁ�'��ʨ��fPT��lɅ�f����;k&�5�bF�����cs�7���XJtG�ly��{P4G6T\q�'X�+Mq���үߢ�ԅ��i��&��g��+�bw�(n_x�,A��/[`�T�b�e���_��Rҹ�4�=t0��ĸ�8��A��ŕ��
~Uq���mFU��M�v��C�w��6i��X�²p=��,s�Y�����]���}���\�L�R��,>�횘��%&�Ӻ �8pg�܀ھ�,�iS��f"�	��v���W�P�o��Ց?�lXC���Y�����>�f�i� 伕��]�'m���w����#z����I��Gȳ�c�� �\�MI��R�(�����ޟb;�|��|w�I��uG�����Y^ۨ���tߧұ��X:�t��[���>l�;K��*���;�����J��T�x��k�3Xwت����1����z��Ek�ޡ���@x� PK��A�  �	  PK  �@�U               word/fontTable.xml�PAN�0��
�w����U%�	�@��d�#�I��q�DB�B�f�����r���0��T����I���S%�����Rp:����<#���nٗ���"��}%��R)�:��o�V�� �o8�އc�F��ZŃr`H2�72����'��R����ܘ��jH'�����{��{��P&��Ӂ�dQH���{�!�3К��q�A0p�x��������Nz-n��I�i�ɳ�7��z1�l��`��
6n:�|�[M%�ߺ��ɀx*ص��3<x�	PK��J�  U  PK  �@�U               word/settings.xmleP�n�@��+�����"��О�`6Y)�^�R��5���z�=3�W���'��)�f1/M��Q��6����,�)bm��f��[���������6�H��e�a �S¨XK9�h��v�ܤL�Uz�,��G�֕_D����a=gY{la�e��PR�	��<�����9uA4��<�Dp�o��nWb�����?�����4
��������\%���;��27��������▢����ʻX^���|��?��w��PK1�	  �  PK  �@�U               [Content_Types].xml���n�0��y
ĵ'颪�����搞+��-^d;i������,�G<��,�I�kQ+0�+���x �ʸ,��u�݆�� �o4� s�MÅs��� �����\A~��h�>id<����"��$y��.K<���Ey��y�*��%g�a��(i�(��Jf;�EMe1*����^��e�c���̟�+>4�K� j^p܆g̨q�T`y󝐸�~ڜ2�fFi�k1��?��4��8�9"�xC��2�%1�Ag��͖�)q�}�9��K�������������Y]{���Z|��mDP.;��qJ�K0�;.�!�q��> W}@�O�X�)���ޚ۹�-���<��`��,s���)4䦄AB����PK*�Jz  4  PK   �@�U�r�D�   �                   _rels/.relsPK   �@�U@�.�g  �               !  docProps/core.xmlPK   �@�U/�h�7  #               �  docProps/app.xmlPK   �@�U�� ��   �                <  docProps/custom.xmlPK   �@�URr���   �                 word/_rels/document.xml.relsPK   �@�U��$[  pY               V  word/document.xmlPK   �@�U^�@��  �              �  word/media/image1.pngPK   �@�Ue�e^  �h               � word/media/image2.pngPK   �@�U�����k  �s               Dg word/media/image3.pngPK   �@�U�e��}  l�               � word/media/image4.pngPK   �@�UW��Y�e  er               BQ word/media/image5.pngPK   �@�U��A�  �	               � word/styles.xmlPK   �@�U��J�  U               �� word/fontTable.xmlPK   �@�U1�	  �               X� word/settings.xmlPK   �@�U*�Jz  4               �� [Content_Types].xmlPK      �  [�                                                                                                                                                                                                                                                                                                                                                                                                                                                                      final-programming-assignment.iml                                                                    0000664 0001750 0001750 00000000704 14341753162 015757  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   <?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager" inherit-compiler-output="true">
    <exclude-output />
    <content url="file://$MODULE_DIR$" />
    <orderEntry type="jdk" jdkName="Python 3.10" jdkType="Python SDK" />
    <orderEntry type="sourceFolder" forTests="false" />
    <orderEntry type="library" name="OpenSCAD Libraries" level="application" />
  </component>
</module>                                                            nba_record_server.py                                                                                0000664 0001750 0001750 00000006611 14342057632 013536  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   """
Author:  Jeff Alkire
Date:    11-30-2022
Purpose: Class to implement nba record server that will listen on a particular
         port and return the record of the given team in the given year.
"""

import os
from socket import *
from threading import Thread
from time import ctime

from season_data import SeasonData
from request_handler import RequestHandler

# CONSTANTS
DATA_DIR = "data-dir"
HOST = "localhost"
PORT = 32123
ADDRESS = (HOST, PORT)
BACKLOG_ALLOWED = 25

# NOT TECHNICALLY A CONSTANT - ALLOWS EXITING SERVER FROM COMMAND LINE
STOP_SERVER = False

def team_from_filename(filename: str):
    """
    Record data is stored in the data directory in the format <team name>.csv
    :param filename: Name of file found in data directory.
    :return: name of the team (as used in dictionary)
    """
    dot_idx = filename.index(".")
    teamname = filename[0:dot_idx].lower().capitalize()
    return teamname

class NbaRecordServerListener(Thread):
    """
    Implements the listener thread for the server.
    """
    def load_data(self,data_dir=DATA_DIR):
        # move into the data directory to read the files there.
        os.chdir(data_dir)
        # Process all files in the data directory.
        for file in os.scandir("."):
            try:
                print("Reading data from: %s" % file.name)

                with open(file.name, "r") as f:
                    # read entire file (they are relatively short)
                    lines = f.readlines()
                    # Skip first line (header info)
                    lines.pop(0)

                    # all data for this team.
                    team_data = []
                    # Store each entry into a SeasonData object and store in a list.
                    for l in lines:
                        team_data.append( SeasonData(l) )

                    # Get team's name from the filename
                    teamname = team_from_filename(file.name)
                    # Cache all tead data for each team.
                    self.DATA_CACHE[teamname] = team_data

            except:
                # Handle errors by ignore them which will cause the file being
                # read to be ignored.
                print("ERROR PROCESSING: %s (ignoring file)" % file.name)
                pass

    def __init__(self):
        Thread.__init__(self)

        # Read data from disk into memory.
        self.DATA_CACHE = {}
        self.load_data()

    def run(self) -> None:
        svr_socket = socket(AF_INET, SOCK_STREAM)
        svr_socket.bind(ADDRESS)
        svr_socket.listen( BACKLOG_ALLOWED )

        while not STOP_SERVER:
            print("Listening for connections on port %d . . ." % PORT)
            client, address = svr_socket.accept()
            print("... connected from: %s at %s" % (address,ctime()))
            req_handler = RequestHandler(client, self.DATA_CACHE)
            req_handler.start()

class QuitThread(Thread):
    """
    A Thread to allow graceful termination of the server after the next request
    is processed.
    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        input("Press enter to exit:\n")
        global STOP_SERVER
        STOP_SERVER = True

def main():
    # Graceful termination thread.
    qt = QuitThread()
    qt.start()

    # Thread to listen for new requests.
    listener = NbaRecordServerListener()
    listener.start()

if __name__ == "__main__":
    main()                                                                                                                       __pycache__/                                                                                        0000775 0001750 0001750 00000000000 14342057741 011705  5                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   __pycache__/request_handler.cpython-310.pyc                                                         0000664 0001750 0001750 00000004141 14342054733 017571  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   o
    �?�c  �                   @   sP   d Z ddlmZ ddlmZ ddlmZmZ ddlm	Z	 dZ
G dd� de�Zd	S )
zV
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Thread to handle a user request.
�    )�decode)�Thread)�Request�build_request_from_message)�Responsei   c                   @   s(   e Zd ZdZdd� Zdd� Zdd� ZdS )	�RequestHandlerzE
    Thread to handles a client request. One thread per request.
    c                 C   s   t �| � || _|| _dS )z.initialize object's connection and data cache.N)r   �__init__�client�cache)�selfr	   r
   � r   �n/media/jeff/Fermium/jeff-home-links/git/Python/CIS-087/week-16/final-programming-assignment/request_handler.pyr      s   

zRequestHandler.__init__c                 C   s\   t | j�t�d��� }t|d �}| �|�}tt|��d }| j�	t
|d�� | j��  dS )z)Process single request and send response.�asciir   �
N)r   r	   �recv�BUFSIZE�splitr   �process�strr   �send�bytes�close)r   �user_request�request�season_data�text_responser   r   r   �run   s   
zRequestHandler.runc                    s6   z| j � j }� fdd�|D �}t|�W S    Y dS )a{  
        Routine to process the request.  Search through the cache for the team
        supplied in the request.  The search all data for this team for the data
        for the specified year.
        param req: Request object with the user's request.
        return: The data for the given team in the given year.  If no data is
                found, None is returned.
        c                 3   s   � | ]	}� |kr|V  qd S )Nr   )�.0�x��reqr   r   �	<genexpr>-   s   � z)RequestHandler.process.<locals>.<genexpr>N)r
   �team�next)r   r    �	team_data�matchesr   r   r   r   "   s   	
zRequestHandler.processN)�__name__�
__module__�__qualname__�__doc__r   r   r   r   r   r   r   r      s
    
r   N)r)   �codecsr   �	threadingr   r   r   r   �responser   r   r   r   r   r   r   �<module>   s                                                                                                                                                                                                                                                                                                                                                                                                                                   __pycache__/request.cpython-310.pyc                                                                 0000664 0001750 0001750 00000003661 14342054733 016102  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   o
    �?�c/  �                   @   s0   d Z ddlmZ defdd�ZG dd� d�ZdS )	z
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of a information request.
�    )�
SeasonData�user_requestc                 C   s   | � d�}t|d |d �S )z�
    Given a user request in comma separated value format, build a request object.
    :param user_request: string version
    :return: request object version
    �,�   �   )�split�Request)r   �entries� r
   �f/media/jeff/Fermium/jeff-home-links/git/Python/CIS-087/week-16/final-programming-assignment/request.py�build_request_from_message	   s   
r   c                   @   s0   e Zd ZdZdd� Zdd� Zdd� Zdd	� Zd
S )r   zB
    Stores all data about a single season for a single team.
    c                 C   s   | � d||� d S )Nr   )�	init_data)�self�team�yearr
   r
   r   �__init__   s   zRequest.__init__c                 C   s   || _ || _|| _d S )N)�versionr   r   )r   �protocol_version�	team_namer   r
   r
   r   r      s   
zRequest.init_datac                 C   s   dd| j | jf S )z! Convert request to a csv string z%d,%s,%sr   )r   r   )r   r
   r
   r   �__str__"   s   zRequest.__str__c                 C   sL   t |�tkr| j|jko| j|jko| j|jkS t |�tkr$|j| jkS dS )z�
        Allows equality check between a user's request and the data in
        a SeasonData object.
        param other: item to compare myself to.
        return: True if there is a match, false if not.
        F)�typer   r   r   r   r   )r   �otherr
   r
   r   �__eq__&   s   
�
�zRequest.__eq__N)�__name__�
__module__�__qualname__�__doc__r   r   r   r   r
   r
   r
   r   r      s    	r   N)r   �season_datar   �strr   r   r
   r
   r
   r   �<module>   s    	                                                                               __pycache__/nba_record_server.cpython-310.pyc                                                       0000664 0001750 0001750 00000006452 14342057640 020077  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   o
    �_�c�  �                   @   s�   d Z ddlZddlT ddlmZ ddlmZ ddlmZ ddl	m
Z
 dZd	Zd
ZeefZdZdadefdd�ZG dd� de�ZG dd� de�Zdd� ZedkrTe�  dS dS )z�
Author:  Jeff Alkire
Date:    11-30-2022
Purpose: Class to implement nba record server that will listen on a particular
         port and return the record of the given team in the given year.
�    N)�*)�Thread)�ctime)�
SeasonData)�RequestHandlerzdata-dir�	localhosti{}  �   F�filenamec                 C   s"   | � d�}| d|� �� �� }|S )z�
    Record data is stored in the data directory in the format <team name>.csv
    :param filename: Name of file found in data directory.
    :return: name of the team (as used in dictionary)
    �.r   )�index�lower�
capitalize)r	   �dot_idx�teamname� r   �p/media/jeff/Fermium/jeff-home-links/git/Python/CIS-087/week-16/final-programming-assignment/nba_record_server.py�team_from_filename   s   
r   c                   @   s.   e Zd ZdZefdd�Zdd� Zd
dd	�ZdS )�NbaRecordServerListenerz8
    Implements the listener thread for the server.
    c              	   C   s�   t �|� t �d�D ]N}z@td|j � t|jd��)}|�� }|�d� g }|D ]	}|�t	|�� q(t
|j�}|| j|< W d   � n1 sFw   Y  W q
   td|j � Y q
d S )Nr
   zReading data from: %s�rr   z$ERROR PROCESSING: %s (ignoring file))�os�chdir�scandir�print�name�open�	readlines�pop�appendr   r   �
DATA_CACHE)�self�data_dir�file�f�lines�	team_data�lr   r   r   r   �	load_data(   s$   


���z!NbaRecordServerListener.load_datac                 C   s   t �| � i | _| ��  d S �N)r   �__init__r   r&   �r   r   r   r   r(   G   s   
z NbaRecordServerListener.__init__�returnNc                 C   sl   t tt�}|�t� |�t� ts4tdt	 � |�
� \}}td|t� f � t|| j�}|��  trd S d S )Nz*Listening for connections on port %d . . .z... connected from: %s at %s)�socket�AF_INET�SOCK_STREAM�bind�ADDRESS�listen�BACKLOG_ALLOWED�STOP_SERVERr   �PORT�acceptr   r   r   �start)r   �
svr_socket�client�address�req_handlerr   r   r   �runN   s   


�zNbaRecordServerListener.run)r*   N)�__name__�
__module__�__qualname__�__doc__�DATA_DIRr&   r(   r:   r   r   r   r   r   $   s
    r   c                   @   s    e Zd ZdZdd� Zdd� ZdS )�
QuitThreadzg
    A Thread to allow graceful termination of the server after the next request
    is processed.
    c                 C   s   t �| � d S r'   )r   r(   r)   r   r   r   r(   _   s   zQuitThread.__init__c                 C   s   t d� dad S )NzPress enter to exit:
T)�inputr2   r)   r   r   r   r:   b   s   zQuitThread.runN)r;   r<   r=   r>   r(   r:   r   r   r   r   r@   Z   s    r@   c                  C   s    t � } | ��  t� }|��  d S r'   )r@   r5   r   )�qt�listenerr   r   r   �maing   s   rD   �__main__)r>   r   r+   �	threadingr   �timer   �season_datar   �request_handlerr   r?   �HOSTr3   r/   r1   r2   �strr   r   r@   rD   r;   r   r   r   r   �<module>   s(    
6	
�                                                                                                                                                                                                                      __pycache__/breezypythongui.cpython-310.pyc                                                         0000664 0001750 0001750 00000110461 14342020004 017636  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   o
    Pn`c��  �                   @   s�  d Z ddlZejjZedkr"ddlZddlZeZejZ	ddlm
Z
 nddlZddl	Z	ddlm
Z
 ejZejZejZejZejZejZejZejZejZejZejZejZejZejZejZG dd� dej�ZG dd� dej�ZG d	d
� d
e�ZG dd� de�ZG dd� de�Z G dd� dej!�Z"G dd� de
j#�Z$G dd� dej%�Z&G dd� dej�Z'G dd� dej(�Z)G dd� dej�Z*G dd� dej+�Z,G dd� de-�Z.G dd � d ej/�Z0G d!d"� d"e	j1�Z2G d#d$� d$e	j1�Z3G d%d&� d&e	j1�Z4G d'd(� d(ej�Z5dS ))a�  
File: breezypythongui.py
Version: 1.2
Copyright 2012, 2013, 2019 by Ken Lambert

Resources for easy Python GUIs.

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).  Its capabilities mirror those 
of BreezyGUI and BreezySwing, open-source frameworks for writing GUIs in Java,
written by Ken Lambert and Martin Osborne.

PLATFORMS: The package is a wrapper around Tkinter (Python 3.X) and should
run on any platform where Tkinter is available.

INSTALLATION: Put this file where Python can see it.

RELEASE NOTES:
Version 1.2 also now includes the class EasyCombobox for
managing combo boxes (updated 08-15-2019).

Version 1.2 also now supports the handling of selections in
multiple list boxes (updated 08-15-2019).

Version 1.2 also now includes the class EasyPanel, for organizing
subpanes in windows and dialogs (updated 12-19-2012).

Version 1.2 now also runs on either Python 3.x.x or
Python 2.x.x (updated 2-4-2013).

�    N�   )�ttkc                
   @   s�  e Zd ZdZ		dAdd�Zdd	� Zd
d� Zdd� Zdd� Zdde	e
 dddfdd�Zdddd� efdd�Zdddde	e efdd�Zddde	e efdd�Zddde	e efdd�Zddd d!efd"d#�Zdde	e d$d� fd%d&�Zdddd!d'd� fd(d)�Z	*	,	dBd-d.�Zddd/d� d*d*dd,edd*f
d0d1�Z		2dCd3d4�Zdde	e e e
 d5d� fd6d7�Zddefd8d9�Z	dDd:d;�ZdEd=d>�ZdFd?d@�Z dS )G�	EasyFramez!Represents an application window.� N�whiteTc                 C   s�   t jj| ddd� |r|r| �||� | j�|� | ��  | jjddd� | jjddd� | jt	t
 t t d� | �|� | �|� dS )	z\Will shrink wrap the window around the widgets if width
        and height are not provided.�   �sunken)�borderwidth�reliefr   �   ��weight)�stickyN)�Tkinter�Frame�__init__�setSize�master�title�grid�rowconfigure�columnconfigure�N�S�E�W�setBackground�setResizable)�selfr   �width�height�
background�	resizable� r#   �n/media/jeff/Fermium/jeff-home-links/git/Python/CIS-087/week-16/final-programming-assignment/breezypythongui.pyr   A   s   
zEasyFrame.__init__c                 C   �   || d< dS )z.Resets the window's background color to color.r!   Nr#   �r   �colorr#   r#   r$   r   R   �   zEasyFrame.setBackgroundc                 C   s   | j �||� dS )z@Resets the window's resizable property to True
        or False.N)r   r"   �r   �stater#   r#   r$   r   V   �   zEasyFrame.setResizablec                 C   s    | j �t|�d t|� � dS )z/Resets the window's width and height in pixels.�xN)r   �geometry�str)r   r   r    r#   r#   r$   r   [   s    zEasyFrame.setSizec                 C   s   | j �|� dS )z#Resets the window's title to title.N)r   r   )r   r   r#   r#   r$   �setTitle_   s   zEasyFrame.setTitler   �blackc
              	   C   �L   t j| ||||	d�}
| j|dd� | j|dd� |
j||||dd|d� |
S ��QCreates and inserts a label at the row and column,
        and returns the label.)�text�fontr!   �
foregroundr   r   �   ��row�column�
columnspan�rowspan�padx�padyr   �r   �Labelr   r   r   �r   r4   r9   r:   r;   r<   r   r5   r!   r6   �labelr#   r#   r$   �addLabelf   �   
��zEasyFrame.addLabelc                   C   �   d S �Nr#   r#   r#   r#   r$   �<lambda>x   �    zEasyFrame.<lambda>c           	      C   �H   t j| |||d�}| j|dd� | j|dd� |j||||ddd� |S �zSCreates and inserts a button at the row and column,
        and returns the button.)r4   �commandr*   r   r   r7   )r9   r:   r;   r<   r=   r>   �r   �Buttonr   r   r   �	r   r4   r9   r:   r;   r<   rK   r*   �buttonr#   r#   r$   �	addButtonv   �   ��zEasyFrame.addButton�   c
              	   C   �H   t | ||||	�}
| j|dd� | j|dd� |
j||||dd|d� |
S �z]Creates and inserts a float field at the row and column,
        and returns the float field.r   r   r7   r8   ��
FloatFieldr   r   r   �r   �valuer9   r:   r;   r<   r   �	precisionr   r*   �fieldr#   r#   r$   �addFloatField�   �   �zEasyFrame.addFloatField�
   c	           
   	   C   �F   t | |||�}	| j|dd� | j|dd� |	j||||dd|d� |	S �zbCreates and inserts an integer field at the row and column,
        and returns the integer field.r   r   r7   r8   ��IntegerFieldr   r   r   �
r   rX   r9   r:   r;   r<   r   r   r*   rZ   r#   r#   r$   �addIntegerField�   �   �zEasyFrame.addIntegerFieldc	           
   	   C   r^   �z[Creates and inserts a text field at the row and column,
        and returns the text field.r   r   r7   r8   ��	TextFieldr   r   r   �
r   r4   r9   r:   r;   r<   r   r   r*   rZ   r#   r#   r$   �addTextField�   rd   zEasyFrame.addTextField�P   r7   c	                 C   ��   t �| �}	|	j||||tt t t d� | j|dd� | j|dd� t j	|	t
d�}
|
jddtt d� t j	|	td�}|jddtt d� t|	||||
j|j|�}|jddddtt t t d� |	jddd� |	jddd� |j|
d	< |j|d	< |S �
z�Creates and inserts a multiline text area at the row and column,
        and returns the text area.  Vertical and horizontal scrollbars are
        provided.�r9   r:   r;   r<   r   r   r   ��orientr   �r9   r:   r   r7   )r9   r:   r=   r>   r   rK   �r   r   r   r   r   r   r   r   r   �	Scrollbar�
HORIZONTAL�VERTICAL�TextArea�set�xview�yview�r   r4   r9   r:   r<   r;   r   r    �wrap�frame�xScroll�yScroll�arear#   r#   r$   �addTextArea�   �,   
�

��

zEasyFrame.addTextAreac                   C   rE   rF   r#   r#   r#   r#   r$   rG   �   rH   c	           
   	   C   �F   t | |||�}	| j|dd� | j|dd� |	j||||dd|d� |	S �zYCreates and inserts a combo box at the row and column,
        and returns the combo box.r   r   r7   r8   ��EasyComboboxr   r   r   �
r   r4   �valuesr9   r:   r;   r<   r   rK   �boxr#   r#   r$   �addCombobox�   rd   zEasyFrame.addComboboxc                 C   �   | S rF   r#   ��indexr#   r#   r$   rG   �   rH   c                 C   ��   t �| �}|j||||tt t t d� | j|dd� | j|dd� t j	|t
d�}	|	jddtt d� t||||	j|�}
|
jddtt t t d� |jddd� |jddd� |
j|	d< |
S �z�Creates and inserts a scrolling list box at the row and column, with a
        width and height in lines and columns of text, and a default item selection
        method, and returns the list box.rm   r   r   rn   r   rp   rK   �r   r   r   r   r   r   r   r   r   rr   rt   �EasyListboxrv   rx   �r   r9   r:   r<   r;   r   r    �listItemSelectedr{   r}   �listBoxr#   r#   r$   �
addListbox�   �   
�
zEasyFrame.addListboxr   ��   �d   c	           	      C   �T   |s
t | |||d�}|j||||tt t t d� | j|dd� | j|dd� |S �zSCreates and inserts a canvas at the row and column,
        and returns the canvas.�r   r    r!   �r9   r:   r<   r;   r   r]   r   ��
EasyCanvasr   r   r   r   r   r   r   �	r   �canvasr9   r:   r<   r;   r   r    r!   r#   r#   r$   �	addCanvas�   �   ��zEasyFrame.addCanvasc                 C   r�   rF   r#   �rX   r#   r#   r$   rG   �   rH   c                 C   �`   t j| |||||	|
||ddd�}| j|dd� | j|dd� |j||||tt t t d� |S �zQCreates and inserts a scale at the row and column,
        and returns the scale.r   r   )
rK   �from_�torB   �lengthro   �
resolution�tickintervalr
   r	   r   r   rm   �	r   �Scaler   r   r   r   r   r   r   �r   r9   r:   r<   r;   rK   r�   r�   rB   r�   ro   r�   r�   �scaler#   r#   r$   �addScale�   �   �
�zEasyFrame.addScale�
horizontalc                 C   �6   |dvrt d��t| |�}|j||||tt d� |S �zWCreates and inserts a menu bar at the row and column,
        and returns the menu bar.)r�   �verticalz%orient must be horizontal or verticalr�   ��
ValueError�EasyMenuBarr   r   r   �r   r9   r:   r<   r;   ro   �menuBarr#   r#   r$   �
addMenuBar  �   
�zEasyFrame.addMenuBarc                   C   �   dS �Nr   r#   r#   r#   r#   r$   rG     rH   c           	   	   C   �D   t | ||�}| j|dd� | j|dd� |j||||dd|d� |S �z]Creates and inserts check button at the row and column,
        and returns the check button.r   r   r7   r8   ��EasyCheckbuttonr   r   r   �	r   r4   r9   r:   r<   r;   r   rK   �cbr#   r#   r$   �addCheckbutton  �   �zEasyFrame.addCheckbuttonc                 C   �   t | |||||�S �z)Creates and returns a radio button group.��EasyRadiobuttonGroup�r   r9   r:   r<   r;   ro   r#   r#   r$   �addRadiobuttonGroup   r+   zEasyFrame.addRadiobuttonGroupc                 C   r�   �zCreates and returns a panel.��	EasyPanel�r   r9   r:   r<   r;   r!   r#   r#   r$   �addPanel&  r+   zEasyFrame.addPanel�   c                 C   �   t | ||||�}|�� S �z{Creates and pops up a message box, with the given title,
        message, and width and height in rows and columns of text.��
MessageBox�modified�r   r   �messager   r    �dlgr#   r#   r$   �
messageBox-  �   zEasyFrame.messageBoxc                 C   r�   )z�Creates and pops up a prompter box, with the given title, prompt,
        input text, and field width in columns of text.
        Returns the text entered at the prompt.)�PrompterBox�getText)r   r   �promptString�	inputText�
fieldWidthr�   r#   r#   r$   �prompterBox5  s   zEasyFrame.prompterBox)r   NNr   T�Nr   r   r   r   r�   r�   r   �r   r   r�   �r   r   r   �r   r   r�   r7   �r   r   r   rR   )!�__name__�
__module__�__qualname__�__doc__r   r   r   r   r/   r   r   rC   �NORMALrP   r   r[   rc   ri   �NONEr   r�   r�   r�   rs   r�   r�   r   r�   rt   r�   r�   r�   r�   r#   r#   r#   r$   r   >   sr    
�
�
�
�

�

�
�
�

�
�

�
�
�
�
�
r   c                   @   �(   e Zd ZdZdd� Zdd� Zdd� ZdS )	�AbstractFieldzPRepresents common features of float fields, integer fields,
    and text fields.c                 C   s0   t �� | _| �|� t jj| || j||d� d S )N)�textvariabler   r*   )r   �	StringVar�var�setValue�Entryr   �r   �parentrX   r   r*   r#   r#   r$   r   B  s   



�zAbstractField.__init__c                 C   �   | j �|� d S rF   �r�   rv   )r   rX   r#   r#   r$   r�   I  �   zAbstractField.setValuec                 C   �
   | j �� S rF   �r�   �get�r   r#   r#   r$   �getValueL  �   
zAbstractField.getValueN)r�   r�   r�   r�   r   r�   r�   r#   r#   r#   r$   r�   >  s
    r�   c                   @   �0   e Zd ZdZdd� Zdd� Zdd� Zdd	� Zd
S )rV   z/Represents a single line box for I/O of floats.c                 C   s    | � |� t�| ||||� d S rF   )�setPrecisionr�   r   )r   r�   rX   r   rY   r*   r#   r#   r$   r   S  s   
zFloatField.__init__c                 C   �   t | �� �S )z]Returns the float contained in the field.
        Raises: ValueError if number format is bad.)�floatr�   r�   r#   r#   r$   �	getNumberW  �   zFloatField.getNumberc                 C   s   | � | j| � dS )z*Replaces the float contained in the field.N)r�   �
_precision�r   �numberr#   r#   r$   �	setNumber\  s   zFloatField.setNumberc                 C   s,   |r|dkrdt |� d | _dS d| _dS )z0Resets the precision for the display of a float.r   z%0.�fz%fN)r.   r  )r   rY   r#   r#   r$   r�   `  s   
zFloatField.setPrecisionN)r�   r�   r�   r�   r   r  r  r�   r#   r#   r#   r$   rV   P  s    rV   c                   @   r�   )	ra   z1Represents a single line box for I/O of integers.c                 C   �   t �| ||||� d S rF   �r�   r   r�   r#   r#   r$   r   k  �   zIntegerField.__init__c                 C   r�   )z_Returns the integer contained in the field.
        Raises: ValueError if number format is bad.)�intr�   r�   r#   r#   r$   r  n  r  zIntegerField.getNumberc                 C   s   | � t|�� dS )z,Replaces the integer contained in the field.N)r�   r.   r  r#   r#   r$   r  s  s   zIntegerField.setNumberN)r�   r�   r�   r�   r   r  r  r#   r#   r#   r$   ra   h  s
    ra   c                   @   r�   )	rg   z0Represents a single line box for I/O of strings.c                 C   r  rF   r	  r�   r#   r#   r$   r   {  r
  zTextField.__init__c                 C   s   | � � S )z*Returns the string contained in the field.)r�   r�   r#   r#   r$   r�   ~  �   zTextField.getTextc                 C   �   | � |� dS )z+Replaces the string contained in the field.N)r�   �r   r4   r#   r#   r$   �setText�  s   zTextField.setTextN)r�   r�   r�   r�   r   r�   r  r#   r#   r#   r$   rg   x  s
    rg   c                   @   r�   )ru   z+Represents a box for I/O of multiline text.c              	   C   s(   t jj| ||||||d� | �|� d S )N)r   r    rz   �xscrollcommand�yscrollcommand)r   �Textr   r  )r   r�   r4   r   r    r  r  rz   r#   r#   r$   r   �  s   
�zTextArea.__init__c                 C   s   | � dt�S )z.Returns the string contained in the text area.�1.0)r�   �ENDr�   r#   r#   r$   r�   �  r(   zTextArea.getTextc                 C   s   | � dt� | �d|� dS )z/Replaces the string contained in the text area.r  N)�deleter  �insertr  r#   r#   r$   r  �  s   zTextArea.setTextc                 C   s   | � t|� dS )zEInserts the text after the string contained in
        the text area.N)r  r  r  r#   r#   r$   �
appendText�  s   zTextArea.appendTextN)r�   r�   r�   r�   r   r�   r  r  r#   r#   r#   r$   ru   �  s    
ru   c                   @   r�   )	r�   zRepresents a combo box.c                 C   sF   t �� | _| �|� tjj| || jd� || d< || d< | �d� d S )N)r�   r�   �postcommandr   )r   r�   r�   r  r   �Comboboxr   �current)r   r�   r4   r�   rK   r#   r#   r$   r   �  s   


�zEasyCombobox.__init__c                 C   r�   rF   r�   r  r#   r#   r$   r  �  r�   zEasyCombobox.setTextc                 C   r�   rF   r�   r�   r#   r#   r$   r�   �  r�   zEasyCombobox.getTextN)r�   r�   r�   r�   r   r  r�   r#   r#   r#   r$   r�   �  s
    	r�   c                   @   sH   e Zd ZdZdd� Zdd� Zdd� Zdd	� Zd
d� Zdd� Z	dd� Z
dS )r�   zRepresents a list box.c              	   C   s2   || _ tjj| ||||tdd� | �d| j� d S )Nr   )r   r    r  �
selectmode�exportselectionz<<ListboxSelect>>)�_listItemSelectedr   �Listboxr   �SINGLE�bind�triggerListItemSelected)r   r�   r   r    r  r�   r#   r#   r$   r   �  s   
�zEasyListbox.__init__c                 C   s0   | � � dkrdS |j}|�� d }| �|� dS )z�Strategy method to respond to an item selection in the list box.
        Runs the client's listItemSelected method with the selected index if
        there is one.r   N)�size�widget�curselectionr  )r   �eventr#  r�   r#   r#   r$   r!  �  s   z#EasyListbox.triggerListItemSelectedc                 C   s$   | � � }t|�dkrdS t|d �S )zLReturns the index of the selected item or -1 if no item
        is selected.r   �����)r$  �lenr  )r   �tupr#   r#   r$   �getSelectedIndex�  s   zEasyListbox.getSelectedIndexc                 C   s   | � � }|dkr
dS | �|�S )zMReturns the selected item or the empty string if no item
        is selected.r&  r   )r)  r�   �r   r�   r#   r#   r$   �getSelectedItem�  s   
zEasyListbox.getSelectedItemc                 C   s(   |dk s
|| � � krdS | �||� dS )z3Selects the item at the index if it's in the range.r   N)r"  �selection_setr*  r#   r#   r$   �setSelectedIndex�  s   zEasyListbox.setSelectedIndexc                 C   s*   | � � dkr| �d� | � � dksdS dS )z$Deletes all items from the list box.r   N)r"  r  r�   r#   r#   r$   �clear�  s   
�zEasyListbox.clearc                 C   s*   | � d| �� d �}||v r|�|�S dS )zKReturns the index of item if it's in the list box,
        or -1 otherwise.r   r   r&  )r�   r"  r�   )r   �itemr(  r#   r#   r$   �getIndex�  s   
zEasyListbox.getIndexN)r�   r�   r�   r�   r   r!  r)  r+  r-  r.  r0  r#   r#   r#   r$   r�   �  s    			r�   c                   @   s8   e Zd ZdZdd� Zdd� fdd�Zdd	� Zd
d� ZdS )r�   zYRepresents a group of radio buttons, only one of which
    is selected at any given time.c                 C   sZ   t j�| |� | j||||tt t t d� t j|d�| _	t
� | _|| _d | _| _d S )Nr�   )r   r   )r   r   r   r   r   r   r   r   r�   �
_commonVar�dict�_buttons�_orient�
_buttonRow�_buttonColumn)r   r�   r9   r:   r<   r;   ro   r#   r#   r$   r   �  s   �zEasyRadiobuttonGroup.__init__c                   C   r�   r�   r#   r#   r#   r#   r$   rG   �  rH   zEasyRadiobuttonGroup.<lambda>c                 C   s�   || j v r	td��tj| |||| jd�}|| j |< |j| j| jtt	 d� | j
tkr;| j| jdd� |  jd7  _|S | j| jdd� |  jd7  _|S )zgCreates a button with the given text and command, adds it to the group,
        and returns the button.z+Button with this label already in the group)r4   rX   rK   �variablerp   r   r   )r3  r�   r   �Radiobuttonr1  r   r5  r6  r   r   r4  rt   r   r   )r   r4   rK   rO   r#   r#   r$   �addRadiobutton�  s   

�

�z#EasyRadiobuttonGroup.addRadiobuttonc                 C   s(   | j �� | jvrtd��| j| j ��  S )Nz No button has been selected yet.)r1  r�   r3  r�   r�   r#   r#   r$   �getSelectedButton  s   z&EasyRadiobuttonGroup.getSelectedButtonc                 C   s   | j �|d � d S )NrX   )r1  rv   )r   rO   r#   r#   r$   �setSelectedButton  s   z&EasyRadiobuttonGroup.setSelectedButtonN)r�   r�   r�   r�   r   r9  r:  r;  r#   r#   r#   r$   r�   �  s    
r�   c                   @   �    e Zd ZdZdd� Zdd� ZdS )r�   zRepresents a check button.c                 C   s&   t �� | _t jj| ||| j|d� d S )N)r4   r7  rK   )r   �IntVar�	_variable�Checkbuttonr   )r   r�   r4   rK   r#   r#   r$   r     s
   

�zEasyCheckbutton.__init__c                 C   s   | j �� dkS )zAReturns True if the button is checked or
        False otherwise.r   )r>  r�   r�   r#   r#   r$   �	isChecked  �   zEasyCheckbutton.isCheckedN)r�   r�   r�   r�   r   r@  r#   r#   r#   r$   r�     s    r�   c                   @   �$   e Zd ZdZdd� Zefdd�ZdS )r�   zRepresents a menu bar.c                 C   s*   || _ d | _| _tjj| |tdd� d S )Nr   r   )r
   r	   )r4  �_row�_columnr   r   r   �RAISED)r   r�   ro   r#   r#   r$   r   '  s   zEasyMenuBar.__init__c                 C   sN   t | ||d�}|j| j| jd� | jdkr|  jd7  _|S |  jd7  _|S )zJCreates and inserts a menu into the
        menubar, and returns the menu.�r*   )r9   r:   r�   r   )�EasyMenubuttonr   rC  rD  r4  )r   r4   r*   �menur#   r#   r$   �addMenu,  s   
�zEasyMenuBar.addMenuN)r�   r�   r�   r�   r   r�   rI  r#   r#   r#   r$   r�   $  s    r�   c                   @   rB  )rG  zRepresents a menu button.c                 C   s4   t jj| |||d� t �| �| _| j| d< d| _d S )N)r4   r*   rH  r&  )r   �
Menubuttonr   �MenurH  �_currentIndex)r   r�   r4   r*   r#   r#   r$   r   ;  s   
�

zEasyMenubutton.__init__c                 C   s,   | j j|||d� |  jd7  _t| | j�S )z(Inserts a menu option in the given menu.)rB   rK   r*   r   )rH  �add_commandrL  �EasyMenuItem)r   r4   rK   r*   r#   r#   r$   �addMenuItemB  s   zEasyMenubutton.addMenuItemN)r�   r�   r�   r�   r   r�   rO  r#   r#   r#   r$   rG  8  s    rG  c                   @   r<  )rN  z)Represents an option in a drop-down menu.c                 C   s   || _ || _d S rF   )�_menu�_index)r   rH  r�   r#   r#   r$   r   L  s   
zEasyMenuItem.__init__c                 C   s   | j jj| j|d� dS )z$Sets the state of the item to state.rF  N)rP  rH  �entryconfigurerQ  r)   r#   r#   r$   �setStateP  �   zEasyMenuItem.setStateN)r�   r�   r�   r�   r   rS  r#   r#   r#   r$   rN  I  s    rN  c                   @   s�   e Zd ZdZ		d dd�Zdd� Zdd	� Zd
d� Zdd� Zdd� Z	dd� Z
	d!dd�Z	d"dd�Z	d"dd�Zd#dd�Zefdd�Zdd� ZdS )$r�   z�Represents a rectangular area for interactive drawing of shapes.
    Supports simple commands for drawing lines, rectangles, and ovals,
    as well as methods for responding to mouse events in the canvas.Nr   c                 C   sR   t jj| ||||d� | �d| j� | �d| j� | �d| j� | �d| j� d S )Nr�   z<Double-Button-1>z<ButtonPress-1>z<ButtonRelease-1>z<B1-Motion>)r   �Canvasr   r   �mouseDoubleClicked�mousePressed�mouseReleased�mouseDragged)r   r�   r   r    r!   r#   r#   r$   r   Z  s   
�zEasyCanvas.__init__c                 C   r�   )zNTriggered when the mouse is
        double-clicked in the area of this canvas.Nr#   �r   r%  r#   r#   r$   rV  j  �   zEasyCanvas.mouseDoubleClickedc                 C   r�   )zGTriggered when the mouse is
        pressed in the area of this canvas.Nr#   rZ  r#   r#   r$   rW  o  r[  zEasyCanvas.mousePressedc                 C   r�   )zHTriggered when the mouse is
        released in the area of this canvas.Nr#   rZ  r#   r#   r$   rX  t  r[  zEasyCanvas.mouseReleasedc                 C   r�   )zGTriggered when the mouse is
        dragged in the area of this canvas.Nr#   rZ  r#   r#   r$   rY  y  r[  zEasyCanvas.mouseDraggedc                 C   �   | d S )z Returns the width of the canvas.r   r#   r�   r#   r#   r$   �getWidth~  r  zEasyCanvas.getWidthc                 C   r\  )z!Returns the height of the canvas.r    r#   r�   r#   r#   r$   �	getHeight�  r  zEasyCanvas.getHeightr0   r   c                 C   �$   | � ||||�}| j|||d� |S )N)�fillr   )�create_line�
itemconfig)r   �x0�y0�x1�y1r`  r   r/  r#   r#   r$   �drawLine�  s   zEasyCanvas.drawLinec                 C   r_  )zVDraws a rectangle with the given corner points,
        outline color, and fill color.��outliner`  )�create_rectanglerb  �r   rc  rd  re  rf  ri  r`  r/  r#   r#   r$   �drawRectangle�  �   zEasyCanvas.drawRectanglec                 C   r_  )zbDraws an ovel within the given corner points,
        with the given outline color and fill color.rh  )�create_ovalrb  rk  r#   r#   r$   �drawOval�  rm  zEasyCanvas.drawOvalc                 C   s    | � ||�}| j|||d� |S )z�Draws the given text (a string) at the given coordinates
        with the given fill color.  The string is centered vertically
        and horizontally at the given coordinates.)r4   r`  )�create_textrb  )r   r4   r,   �yr`  r/  r#   r#   r$   �drawText�  s   zEasyCanvas.drawTextc                 C   s&   | j ||||d�}| j|||d� |S )z�Draws the given image (a PhotoImage) at the given coordinates.
        The image is centered at the given coordinates by default.)�image�anchor)�create_imagerb  )r   rs  r,   rq  rt  r/  r#   r#   r$   �	drawImage�  s
   
�zEasyCanvas.drawImagec                 C   r  )zPRemoves and erases the shape with the given item
        number from the canvas.N)r  )r   r/  r#   r#   r$   �
deleteItem�  rA  zEasyCanvas.deleteItem)NNr   )r0   r   )r0   N)r0   )r�   r�   r�   r�   r   rV  rW  rX  rY  r]  r^  rg  rl  ro  rr  �CENTERrv  rw  r#   r#   r#   r$   r�   U  s(    
�
�
�	
�
r�   c                   @   sF   e Zd ZdZeddd��Zdd� Zd	d
� Zdd� Zdd� Z	dd� Z
dS )r�   z8Represents a message dialog with a scrollable text area.r   r�   r7   c                 C   s   t t�� ||||� d S rF   )r�   r   r   )�clsr   r�   r   r    r#   r#   r$   r�   �  rT  zMessageBox.messagec                 C   �,   || _ || _|| _d| _tj�| ||� dS �zSet up the window and widgets.FN)�_message�_width�_height�	_modified�tkSimpleDialog�Dialogr   )r   r�   r   r�   r   r    r#   r#   r$   r   �  �
   zMessageBox.__init__c              	   C   s�   | � dd� tj|td�}|jddtt d� tj|| j| j	ddt
|jd�}|jddtt t t d� |�d| j� t|d< |j|d	< |S )
Nr   rn   r   rp   r7   )r   r    r=   r>   rz   r  r  r*   rK   )r"   r   rr   rt   r   r   r   r  r}  r~  �WORDrv   r   r   r  r|  �DISABLEDrx   )r   r   r}   �outputr#   r#   r$   �body�  s   �
zMessageBox.bodyc                 C   �B   t �| �}t j|dd| jtd�}|��  | �d| j� |��  dS �zQadd standard button box.
        override if you do not want the standard buttons�OKr]   )r4   r   rK   �defaultz<Return>N�r   r   rM   �ok�ACTIVE�packr   �r   r�   �wr#   r#   r$   �	buttonbox�  �   

�zMessageBox.buttonboxc                 C   �
   d| _ dS �zQuits the dialog.TN�r  r�   r#   r#   r$   �apply�  �   
zMessageBox.applyc                 C   �   | j S rF   r�  r�   r#   r#   r$   r�   �  �   zMessageBox.modifiedNr�   )r�   r�   r�   r�   �classmethodr�   r   r�  r�  r�  r�   r#   r#   r#   r$   r�   �  s    
r�   c                   @   sN   e Zd ZdZeddd��Zdd� Zdd	� Zd
d� Zdd� Z	dd� Z
dd� ZdS )r�   z-Represents an input dialog with a text field.r   rR   c                 C   s   t t�� ||||�}|�� S )z$Creates and pops up an input dialog.)r�   r   r   r�   )ry  r   r�   r�   r�   r�   r#   r#   r$   �prompt�  s   zPrompterBox.promptc                 C   rz  r{  )�_prompt�_textr}  r  r�  r�  r   )r   r�   r   r�   r�   r�   r#   r#   r$   r   �  r�  zPrompterBox.__init__c                 C   st   | � dd� tj|| jd�}|jdddtt t t d� t	|| j
| jt�| _| jjdddtt t t d� | jS )Nr   )r4   r7   )r9   r:   r=   r   r   )r"   r   r@   r�  r   r   r   r   r   rg   r�  r}  r�   �_field)r   r   rB   r#   r#   r$   r�  �  s    zPrompterBox.bodyc                 C   r�  r�  r�  r�  r#   r#   r$   r�  �  r�  zPrompterBox.buttonboxc                 C   r�  r�  r�  r�   r#   r#   r$   r�    r�  zPrompterBox.applyc                 C   r�  rF   r�  r�   r#   r#   r$   r�     r�  zPrompterBox.modifiedc                 C   r�   )z-Returns the text currently in the text field.)r�  r�   r�   r#   r#   r$   r�   
  r�  zPrompterBox.getTextNr�   )r�   r�   r�   r�   r�  r�  r   r�  r�  r�  r�   r�   r#   r#   r#   r$   r�   �  s    
r�   c                
   @   sn  e Zd ZdZd9dd�Zdd� Zdd� Zd	d	ee d
fdd�Z	d	d	dd� e
fdd�Zd	d	dd
ee e
fdd�Zd	d	dee e
fdd�Zd	d	dee e
fdd�Zd	d	ee e e dd� fdd�Zd	d	efdd�Zd	d	dd� dddd ed	df
d!d"�Zd	d	d#d$efd%d&�Zd	d	ee d'd� fd(d)�Zd	d	dd$d*d� fd+d,�Z		 	.d:d/d0�Z			1d;d2d3�Zd<d5d6�Z	.d=d7d8�Zd
S )>�
EasyDialogz[Represents a general-purpose dialog.  Subclasses should include
    body and apply methods.r   c                 C   s   d| _ tj�| ||� dS r{  )r  r�  r�  r   )r   r�   r   r#   r#   r$   r     s   zEasyDialog.__init__c                 C   r�  )z*Returns the modified status of the dialog.r�  r�   r#   r#   r$   r�     s   zEasyDialog.modifiedc                 C   s
   d| _ d S )NTr�  r�   r#   r#   r$   �setModified  r�   zEasyDialog.setModifiedr   Nc	           
   	   C   sH   t j|||d�}	|j|dd� |j|dd� |	j||||dd|d� |	S )r3   )r4   r5   r   r   r7   r8   r?   )
r   r   r4   r9   r:   r;   r<   r   r5   rB   r#   r#   r$   rC     s   �zEasyDialog.addLabelc                   C   rE   rF   r#   r#   r#   r#   r$   rG   -  rH   zEasyDialog.<lambda>c	           
      C   sH   t j||||d�}	|j|dd� |j|dd� |	j||||ddd� |	S rJ   rL   )
r   r   r4   r9   r:   r;   r<   rK   r*   rO   r#   r#   r$   rP   +  rQ   zEasyDialog.addButtonrR   c              	   C   sH   t |||||
�}|j|dd� |j|dd� |j||||dd|	d� |S rT   rU   )r   r   rX   r9   r:   r;   r<   r   rY   r   r*   rZ   r#   r#   r$   r[   :  r\   zEasyDialog.addFloatFieldr]   c
              	   C   �F   t ||||	�}
|j|dd� |j|dd� |
j||||dd|d� |
S r_   r`   )r   r   rX   r9   r:   r;   r<   r   r   r*   rZ   r#   r#   r$   rc   H  rd   zEasyDialog.addIntegerFieldc
              	   C   r�  re   rf   )r   r   r4   r9   r:   r;   r<   r   r   r*   rZ   r#   r#   r$   ri   U  rd   zEasyDialog.addTextFieldc                   C   r�   r�   r#   r#   r#   r#   r$   rG   d  rH   c	           
   	   C   sD   t |||�}	|j|dd� |j|dd� |	j||||dd|d� |	S r�   r�   )
r   r   r4   r9   r:   r<   r;   r   rK   r�   r#   r#   r$   r�   b  r�   zEasyDialog.addCheckbuttonc                 C   �   t ||||||�S r�   r�   )r   r   r9   r:   r<   r;   ro   r#   r#   r$   r�   o  r+   zEasyDialog.addRadiobuttonGroupc                 C   r�   rF   r#   r�   r#   r#   r$   rG   u  rH   r   r�   c                 C   s`   t j|||||	|
|||ddd�}|j|dd� |j|dd� |j||||tt t t d� |S r�   r�   )r   r   r9   r:   r<   r;   rK   r�   r�   rB   r�   ro   r�   r�   r�   r#   r#   r$   r�   t  r�   zEasyDialog.addScalerj   r7   c
                 C   s�   t �|�}
|
j||||tt t t d� |j|dd� |j|dd� t j	|
t
d�}|jddtt d� t j	|
td�}|jddtt d� t|
||||j|j|	�}|jddddtt t t d� |
jddd� |
jddd� |j|d	< |j|d	< |S rl   rq   )r   r   r4   r9   r:   r<   r;   r   r    rz   r{   r|   r}   r~   r#   r#   r$   r   �  r�   zEasyDialog.addTextAreac                   C   rE   rF   r#   r#   r#   r#   r$   rG   �  rH   c	           
   	   C   r�   r�   r�   r�   r#   r#   r$   r�   �  rd   zEasyDialog.addComboboxc                 C   r�   rF   r#   r�   r#   r#   r$   rG   �  rH   c	                 C   s�   t �|�}	|	j||||tt t t d� |j|dd� |j|dd� t j	|	t
d�}
|
jddtt d� t|	|||
j|�}|jddtt t t d� |	jddd� |	jddd� |j|
d< |S r�   r�   )r   r   r9   r:   r<   r;   r   r    r�   r{   r}   r�   r#   r#   r$   r�   �  r�   zEasyDialog.addListboxr�   r   c
           
      C   sT   |s
t ||||	d�}|j||||tt t t d� |j|dd� |j|dd� |S r�   r�   )
r   r   r�   r9   r:   r<   r;   r   r    r!   r#   r#   r$   r�   �  r�   zEasyDialog.addCanvasr�   c                 C   s6   |dvrt d��t||�}|j||||tt d� |S r�   r�   )r   r   r9   r:   r<   r;   ro   r�   r#   r#   r$   r�   �  r�   zEasyDialog.addMenuBarr�   c                 C   r�   r�   r�   r�   r#   r#   r$   r�   �  r�   zEasyDialog.messageBoxc                 C   r�  r�   r�   )r   r   r9   r:   r<   r;   r!   r#   r#   r$   r�   �  r+   zEasyDialog.addPanel)r   r�   r�   r�   r�   )r�   r�   r�   r�   r   r�   r�  r   r   rC   r�   rP   r   r[   rc   ri   r   r�   rt   r�   rs   r�   r�   r   r�   r�   r�   r�   r�   r�   r#   r#   r#   r$   r�    sf    

�
�
�

�

�
�
�

�
�
�

�
�
�
�r�  c                
   @   s^  e Zd ZdZdd� Zdd� Zdddd� efd	d
�Zddee	 dddfdd�Z
ddddee efdd�Zdddee efdd�Zdddee efdd�Zddddefdd�Zddee dd� fdd�Zdddddd� fd d!�Z	"	$	d5d%d&�Zddd'd� d"d"d(d$edd"f
d)d*�Z		+d6d,d-�Zddee e e	 d.d� fd/d0�Zddefd1d2�Z	d7d3d4�ZdS )8r�   z7Organizes a group of widgets in a panel (nested frame).c                 C   sX   t j�| |� |j|dd� |j|dd� | j||||tt t t	 d� | �
|� d S )Nr   r   r�   )r   r   r   r   r   r   r   r   r   r   r   )r   r�   r9   r:   r<   r;   r!   r#   r#   r$   r   �  s   �zEasyPanel.__init__c                 C   r%   )z-Resets the panel's background color to color.r!   Nr#   r&   r#   r#   r$   r   �  r(   zEasyPanel.setBackgroundr   c                   C   rE   rF   r#   r#   r#   r#   r$   rG   �  rH   zEasyPanel.<lambda>c           	      C   rI   rJ   rL   rN   r#   r#   r$   rP   �  rQ   zEasyPanel.addButtonNr   r0   c
              	   C   r1   r2   r?   rA   r#   r#   r$   rC     rD   zEasyPanel.addLabelrR   c
              	   C   rS   rT   rU   rW   r#   r#   r$   r[     r\   zEasyPanel.addFloatFieldr]   c	           
   	   C   r^   r_   r`   rb   r#   r#   r$   rc   &  rd   zEasyPanel.addIntegerFieldc	           
   	   C   r^   re   rf   rh   r#   r#   r$   ri   3  rd   zEasyPanel.addTextFieldrj   r7   c	                 C   rk   rl   rq   ry   r#   r#   r$   r   @  r�   zEasyPanel.addTextAreac                   C   rE   rF   r#   r#   r#   r#   r$   rG   \  rH   c	           
   	   C   r�   r�   r�   r�   r#   r#   r$   r�   Z  rd   zEasyPanel.addComboboxc                 C   r�   rF   r#   r�   r#   r#   r$   rG   h  rH   c                 C   r�   r�   r�   r�   r#   r#   r$   r�   g  r�   zEasyPanel.addListboxr   r�   r�   c	           	      C   r�   r�   r�   r�   r#   r#   r$   r�   z  r�   zEasyPanel.addCanvasc                 C   r�   rF   r#   r�   r#   r#   r$   rG   �  rH   r   c                 C   r�   r�   r�   r�   r#   r#   r$   r�   �  r�   zEasyPanel.addScaler�   c                 C   r�   r�   r�   r�   r#   r#   r$   r�   �  r�   zEasyPanel.addMenuBarc                   C   r�   r�   r#   r#   r#   r#   r$   rG   �  rH   c           	   	   C   r�   r�   r�   r�   r#   r#   r$   r�   �  r�   zEasyPanel.addCheckbuttonc                 C   r�   r�   r�   r�   r#   r#   r$   r�   �  r+   zEasyPanel.addRadiobuttonGroupc                 C   r�   r�   r�   r�   r#   r#   r$   r�   �  r+   zEasyPanel.addPanelr�   r�   r�   )r�   r�   r�   r�   r   r   r�   rP   r   r   rC   r   r[   rc   ri   r�   r   r�   r�   r�   rs   r�   r�   r   r�   rt   r�   r�   r#   r#   r#   r$   r�   �  sd    	
�
�
�

�

�
�
�

�
�

�
�
�
��r�   )6r�   �sys�version_info�major�versionNumber�tkinter�tkinter.simpledialogr   �simpledialogr�  r   r   r   r   r   rx  r  r�   r�  r�   r�  rt   rs   rE  r  r�  r   r   r�   r�   rV   ra   rg   r  ru   r  r�   r  r�   r�   r?  r�   r�   rJ  rG  �objectrN  rU  r�   r�  r�   r�   r�  r�   r#   r#   r#   r$   �<module>   s`       9)^-. \                                                                                                                                                                                                               __pycache__/response.cpython-310.pyc                                                                0000664 0001750 0001750 00000003465 14342057741 016254  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   o
    �_�c{  �                   @   s0   d Z ddlmZ defdd�ZG dd� d�ZdS )	z�
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of the server's
         response to a data request.
�    )�
SeasonData�user_requestc                 C   sB   | � d�}|�d� d�|�}|d dks|d dkrd}t|�S )z�
    Given a comma separated message, build a response object.
    :param user_request:  The message is csv format
    :return: the data as a SeasonData object
    �,r   � zData,,not,Available,,,,,,)�split�pop�joinr   )r   �entries�message� r   �g/media/jeff/Fermium/jeff-home-links/git/Python/CIS-087/week-16/final-programming-assignment/response.py�build_response_from_message
   s   


r   c                   @   s&   e Zd ZdZdefdd�Zdd� ZdS )�ResponsezB
    Stores all data about a single season for a single team.
    �season_infoc                 C   s&   d| _ |d krtd�| _d S || _d S )N�   z	,,,,,,,,,)�versionr   �data)�selfr   r   r   r   �__init__   s   
zResponse.__init__c                 C   sB   d| j | jj| jj| jj| jj| jj| jj| jj| jj	| jj
f
 S )z�
        Convert info into a string for easier transference between the
        client and server.
        return: A string representation of the response object.
        z%d,%s,%s,%s,%s,%s,%s,%s,%s,%s)r   r   �year�league_name�	team_name�wins�losses�win_percentage�playoff_results�
coach_name�best_player)r   r   r   r   �__str__#   s   ��zResponse.__str__N)�__name__�
__module__�__qualname__�__doc__r   r   r   r   r   r   r   r      s    r   N)r"   �season_datar   �strr   r   r   r   r   r   �<module>   s                                                                                                                                                                                                               __pycache__/season_data.cpython-310.pyc                                                             0000664 0001750 0001750 00000002333 14342055003 016655  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   o
    �Y�c+  �                   @   s   d Z G dd� d�ZdS )z�
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of a single basketball season.
c                   @   s    e Zd ZdZdd� Zdd� ZdS )�
SeasonDatazB
    Stores all data about a single season for a single team.
    c                 C   s`   |� d�}|d d d� |d< | �|d |d |d |d |d |d	 |d
 |d |d �	 d S )N�,�   ������    �   �   �   �   �   �   �   )�split�	init_data)�self�line_from_csv_file�entries� r   �j/media/jeff/Fermium/jeff-home-links/git/Python/CIS-087/week-16/final-programming-assignment/season_data.py�__init__   s   

�zSeasonData.__init__c
           
      C   s:   || _ || _|| _|| _|| _|| _|| _|| _|	| _d S )N)	�year�league_name�	team_name�wins�losses�win_percentage�playoff_results�
coach_name�best_player)
r   r   r   r   r   r   r   r   r   r   r   r   r   r      s   

zSeasonData.init_dataN)�__name__�
__module__�__qualname__�__doc__r   r   r   r   r   r   r      s    r   N)r!   r   r   r   r   r   �<module>   s                                                                                                                                                                                                                                                                                                         request_handler.py                                                                                  0000664 0001750 0001750 00000003022 14342037644 013231  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   """
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Thread to handle a user request.
"""
from codecs import decode
from threading import Thread

from request import Request, build_request_from_message
from response import Response

BUFSIZE = 1024

class RequestHandler(Thread):
    """
    Thread to handles a client request. One thread per request.
    """
    def __init__(self, client, cache):
        """initialize object's connection and data cache."""
        Thread.__init__(self)
        self.client = client
        self.cache = cache

    def run(self):
        """Process single request and send response."""
        user_request = decode(self.client.recv(BUFSIZE), "ascii").split()
        request = build_request_from_message(user_request[0])
        season_data = self.process(request)
        text_response = str(Response(season_data)) + "\n"
        self.client.send(bytes(text_response,"ascii"))

        self.client.close()

    def process(self,req):
        """
        Routine to process the request.  Search through the cache for the team
        supplied in the request.  The search all data for this team for the data
        for the specified year.
        param req: Request object with the user's request.
        return: The data for the given team in the given year.  If no data is
                found, None is returned.
        """
        try:
            team_data = self.cache[req.team]
            matches = (x for x in team_data if req==x)
            return next(matches)
        except:
            return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              request.py                                                                                          0000664 0001750 0001750 00000003057 14342037615 011542  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   """
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of a information request.
"""

from season_data import SeasonData

def build_request_from_message(user_request: str):
    """
    Given a user request in comma separated value format, build a request object.
    :param user_request: string version
    :return: request object version
    """
    entries = user_request.split(",")
    return Request( entries[1],entries[2])

class Request:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self,team,year):
        self.init_data(1,team,year)

    def init_data(self,
                  protocol_version,
                  team_name,
                  year
                  ):
        self.version = protocol_version
        self.team = team_name
        self.year = year

    def __str__(self):
        """ Convert request to a csv string """
        return "%d,%s,%s" % (1,self.team,self.year)

    def __eq__(self,other):
        """
        Allows equality check between a user's request and the data in
        a SeasonData object.
        param other: item to compare myself to.
        return: True if there is a match, false if not.
        """
        if type(other) == Request:
            return self.protocol_version == other.protocol_version and \
                   self.team_name == other.team_name and \
                   self.year == other.year

        elif type(other) == SeasonData:
            return other.year == self.year

        else:
            return False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 response.py                                                                                         0000664 0001750 0001750 00000003173 14342057735 011714  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   """
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of the server's
         response to a data request.
"""

from season_data import SeasonData

def build_response_from_message(user_request: str):
    """
    Given a comma separated message, build a response object.
    :param user_request:  The message is csv format
    :return: the data as a SeasonData object
    """
    entries = user_request.split(",")
    entries.pop(0)
    message = ",".join(entries)

    if message[0]=="" or message[0]==",":
        message="Data,,not,Available,,,,,,"
    return SeasonData(message)

class Response:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self, season_info: SeasonData):
        self.version = 1
        if season_info == None:
            self.data = SeasonData(",,,,,,,,,")
        else:
            self.data = season_info

    def __str__(self):
        """
        Convert info into a string for easier transference between the
        client and server.
        return: A string representation of the response object.
        """
        return "%d,%s,%s,%s,%s,%s,%s,%s,%s,%s" \
                    % ( self.version,
                        self.data.year,
                        self.data.league_name,
                        self.data.team_name,
                        self.data.wins,
                        self.data.losses,
                        self.data.win_percentage,
                        self.data.playoff_results,
                        self.data.coach_name,
                        self.data.best_player
                       )
                                                                                                                                                                                                                                                                                                                                                                                                     season_data.py                                                                                      0000664 0001750 0001750 00000003053 14342054773 012333  0                                                                                                    ustar   jeff                            jeff                                                                                                                                                                                                                   """
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of a single basketball season.
"""

class SeasonData:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self, line_from_csv_file):
        entries = line_from_csv_file.split(",")
        # Prune /n off end of each line
        entries[8] = entries[8][:-1]
        # Store each entry into a SeasonData object and store in a list.
        self.init_data( entries[0], # year
                        entries[1], # league
                        entries[2], # team name
                        entries[3], # wins
                        entries[4], # losses
                        entries[5], # win %
                        entries[6], # playoff results
                        entries[7], # coach(es)
                        entries[8]  # best player
                      )

    def init_data(self, year,
                        league_name,
                        team_name,
                        wins,
                        losses,
                        win_percentage,
                        playoff_results,
                        coach_name,
                        best_player
                 ):
        self.year = year
        self.league_name = league_name
        self.team_name = team_name
        self.wins = wins
        self.losses = losses
        self.win_percentage = win_percentage
        self.playoff_results = playoff_results
        self.coach_name = coach_name
        self.best_player = best_player                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     