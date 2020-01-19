"""
Unit tests for the OOP version of the CSV processor.
"""

import io
import textwrap

from csv_processor.process_csv_files import CsvProcessor


class TestProcessCsvFiles:
    csv_processor: CsvProcessor

    def setup_method(self, method):
        self.csv_processor = CsvProcessor()

    def test_read_csv_file_file_success(self):
        csv_file_path = 'hvbp_clinical_care.csv'

        results = self.csv_processor.read_csv_file(csv_file_path)
    
        assert len(results) == 5
        assert results[0] == ["010001", "SOUTHEAST ALABAMA MEDICAL CENTER", "1108 ROSS CLARK CIRCLE",
                              "DOTHAN", "AL", "36301", "Houston", "0.866270", "7 out of 10"]
        assert results[4] == ["010011", "ST VINCENT'S EAST", "50 MEDICAL PARK EAST DRIVE",
                              "BIRMINGHAM", "AL", "35235", "Jefferson", "0.863407", "6 out of 10"]
    
    def test_process_csv_stream_success(self):
        csv_text = textwrap.dedent("""\
            Provider Number,Hospital Name,Address,City,State,ZIP Code
            010001,SOUTHEAST ALABAMA MEDICAL CENTER,1108 ROSS CLARK CIRCLE,DOTHAN,AL,36301
            010005,MARSHALL MEDICAL CENTER SOUTH,2505 U S HIGHWAY 431 NORTH,BOAZ,AL,35957
            010006,ELIZA COFFEE MEMORIAL HOSPITAL,205 MARENGO STREET,FLORENCE,AL,35631
            010007,MIZELL MEMORIAL HOSPITAL,702 N MAIN ST,OPP,AL,36467
            010011,ST VINCENT'S EAST,50 MEDICAL PARK EAST DRIVE,BIRMINGHAM,AL,35235
        """)
        csv_input_stream = io.StringIO(csv_text)

        results = self.csv_processor.process_csv_stream(csv_input_stream)

        assert len(results) == 5
        assert results[0] == ["010001", "SOUTHEAST ALABAMA MEDICAL CENTER",
                              "1108 ROSS CLARK CIRCLE", "DOTHAN", "AL", "36301"]
        assert results[4] == ["010011", "ST VINCENT'S EAST",
                              "50 MEDICAL PARK EAST DRIVE", "BIRMINGHAM", "AL", "35235"]

    def test_read_excel_csv_stream_success(self):
        csv_text = '''\
            "Provider Number","Hospital Name","Address","City","State","ZIP Code","County Name","MORT-30-AMI Performance Rate","MORT-30-AMI Achievement Points"
            "010001","SOUTHEAST ALABAMA MEDICAL CENTER","1108 ROSS CLARK CIRCLE","DOTHAN","AL","36301","Houston",0.866270,"7 out of 10"
            "010005","MARSHALL MEDICAL CENTER SOUTH","2505 U S HIGHWAY 431 NORTH","BOAZ","AL","35957","Marshall",0.857280,"3 out of 10"
            "010006","ELIZA COFFEE MEMORIAL HOSPITAL","205 MARENGO STREET","FLORENCE","AL","35631","Lauderdale",0.843841,"0 out of 10"
            "010007","MIZELL MEMORIAL HOSPITAL","702 N MAIN ST","OPP","AL","36467","Covington",0.867181,"7 out of 10"
            "010011","ST VINCENT'S EAST","50 MEDICAL PARK EAST DRIVE","BIRMINGHAM","AL","35235","Jefferson",0.863407,"6 out of 10"
        '''
        csv_input_stream = io.StringIO(textwrap.dedent(csv_text))

        header, result = self.csv_processor.read_excel_csv_stream(csv_input_stream)

        assert header == ["Provider Number", "Hospital Name", "Address", "City", "State", "ZIP Code", "County Name",
                          "MORT-30-AMI Performance Rate", "MORT-30-AMI Achievement Points"]
        assert len(result) == 5
        assert result[0][1] == "SOUTHEAST ALABAMA MEDICAL CENTER"
        assert result[4][1] == "ST VINCENT'S EAST"

    def test_facilities_with_highest_performance_rate_by_column_index(self):
        input_records = [
            ["010001","SOUTHEAST ALABAMA MEDICAL CENTER","1108 ROSS CLARK CIRCLE","DOTHAN","AL","36301","Houston",0.866270,"7 out of 10"],
            ["010005","MARSHALL MEDICAL CENTER SOUTH","2505 U S HIGHWAY 431 NORTH","BOAZ","AL","35957","Marshall",0.857280,"3 out of 10"],
            ["010006","ELIZA COFFEE MEMORIAL HOSPITAL","205 MARENGO STREET","FLORENCE","AL","35631","Lauderdale",0.843841,"0 out of 10"],
            ["010007","MIZELL MEMORIAL HOSPITAL","702 N MAIN ST","OPP","AL","36467","Covington",0.867181,"7 out of 10"],
            ["010011","ST VINCENT'S EAST","50 MEDICAL PARK EAST DRIVE","BIRMINGHAM","AL","35235","Jefferson",0.863407,"6 out of 10"],
        ]

        results = self.csv_processor.facilities_with_max_value_by_column_index(input_records, 7)

        assert results == [
            ["010007", "MIZELL MEMORIAL HOSPITAL", "702 N MAIN ST", "OPP", "AL", "36467", "Covington", 0.867181, "7 out of 10"]
        ]

    def test_facilities_with_highest_achievement_points_by_column_index(self):
        input_records = [
            ["010001","SOUTHEAST ALABAMA MEDICAL CENTER","1108 ROSS CLARK CIRCLE","DOTHAN","AL","36301","Houston",0.866270,"7 out of 10"],
            ["010005","MARSHALL MEDICAL CENTER SOUTH","2505 U S HIGHWAY 431 NORTH","BOAZ","AL","35957","Marshall",0.857280,"3 out of 10"],
            ["010006","ELIZA COFFEE MEMORIAL HOSPITAL","205 MARENGO STREET","FLORENCE","AL","35631","Lauderdale",0.843841,"0 out of 10"],
            ["010007","MIZELL MEMORIAL HOSPITAL","702 N MAIN ST","OPP","AL","36467","Covington",0.867181,"7 out of 10"],
            ["010011","ST VINCENT'S EAST","50 MEDICAL PARK EAST DRIVE","BIRMINGHAM","AL","35235","Jefferson",0.863407,"6 out of 10"],
        ]

        results = self.csv_processor.facilities_with_max_value_by_column_index(input_records, 8)

        assert results == [
            ["010001", "SOUTHEAST ALABAMA MEDICAL CENTER", "1108 ROSS CLARK CIRCLE", "DOTHAN", "AL", "36301", "Houston", 0.866270, "7 out of 10"],
            ["010007", "MIZELL MEMORIAL HOSPITAL", "702 N MAIN ST", "OPP", "AL", "36467", "Covington", 0.867181, "7 out of 10"],
        ]

    def test_facilities_with_highest_performance_rate_by_column_name(self):
        csv_text = '''\
            "Provider Number","Hospital Name","Address","City","State","ZIP Code","County Name","MORT-30-AMI Performance Rate","MORT-30-AMI Achievement Points"
            "010001","SOUTHEAST ALABAMA MEDICAL CENTER","1108 ROSS CLARK CIRCLE","DOTHAN","AL","36301","Houston",0.866270,"7 out of 10"
            "010005","MARSHALL MEDICAL CENTER SOUTH","2505 U S HIGHWAY 431 NORTH","BOAZ","AL","35957","Marshall",0.857280,"3 out of 10"
            "010006","ELIZA COFFEE MEMORIAL HOSPITAL","205 MARENGO STREET","FLORENCE","AL","35631","Lauderdale",0.843841,"0 out of 10"
            "010007","MIZELL MEMORIAL HOSPITAL","702 N MAIN ST","OPP","AL","36467","Covington",0.867181,"7 out of 10"
            "010011","ST VINCENT'S EAST","50 MEDICAL PARK EAST DRIVE","BIRMINGHAM","AL","35235","Jefferson",0.863407,"6 out of 10"
        '''
        csv_input_stream = io.StringIO(textwrap.dedent(csv_text))

        results = self.csv_processor.facilities_with_max_value_from_stream(csv_input_stream, "MORT-30-AMI Performance Rate")

        assert results == [
            ["010007", "MIZELL MEMORIAL HOSPITAL", "702 N MAIN ST", "OPP", "AL", "36467", "Covington", 0.867181, "7 out of 10"]
        ]

    def test_facilities_with_highest_achievement_points_by_column_name(self):
        csv_text = '''\
            "Provider Number","Hospital Name","Address","City","State","ZIP Code","County Name","MORT-30-AMI Performance Rate","MORT-30-AMI Achievement Points"
            "010001","SOUTHEAST ALABAMA MEDICAL CENTER","1108 ROSS CLARK CIRCLE","DOTHAN","AL","36301","Houston",0.866270,"7 out of 10"
            "010005","MARSHALL MEDICAL CENTER SOUTH","2505 U S HIGHWAY 431 NORTH","BOAZ","AL","35957","Marshall",0.857280,"3 out of 10"
            "010006","ELIZA COFFEE MEMORIAL HOSPITAL","205 MARENGO STREET","FLORENCE","AL","35631","Lauderdale",0.843841,"0 out of 10"
            "010007","MIZELL MEMORIAL HOSPITAL","702 N MAIN ST","OPP","AL","36467","Covington",0.867181,"7 out of 10"
            "010011","ST VINCENT'S EAST","50 MEDICAL PARK EAST DRIVE","BIRMINGHAM","AL","35235","Jefferson",0.863407,"6 out of 10"
        '''
        csv_input_stream = io.StringIO(textwrap.dedent(csv_text))

        results = self.csv_processor.facilities_with_max_value_from_stream(csv_input_stream, "MORT-30-AMI Achievement Points")

        assert results == [
            ["010001", "SOUTHEAST ALABAMA MEDICAL CENTER", "1108 ROSS CLARK CIRCLE", "DOTHAN", "AL", "36301", "Houston", 0.866270, "7 out of 10"],
            ["010007", "MIZELL MEMORIAL HOSPITAL", "702 N MAIN ST", "OPP", "AL", "36467", "Covington", 0.867181, "7 out of 10"],
        ]

    def test_facilities_with_highest_performance_rate_from_file(self):
        csv_file_path = 'hvbp_clinical_care.csv'

        results = self.csv_processor.facilities_with_max_value(csv_file_path, "MORT-30-AMI Performance Rate")

        assert results == [
            ["010007", "MIZELL MEMORIAL HOSPITAL", "702 N MAIN ST", "OPP", "AL", "36467", "Covington", 0.867181, "7 out of 10"]
        ]

    def test_facilities_with_highest_achievement_points_from_file(self):
        csv_file_path = 'hvbp_clinical_care.csv'

        results = self.csv_processor.facilities_with_max_value(csv_file_path, "MORT-30-AMI Achievement Points")

        assert results == [
            ["010001", "SOUTHEAST ALABAMA MEDICAL CENTER", "1108 ROSS CLARK CIRCLE", "DOTHAN", "AL", "36301", "Houston", 0.866270, "7 out of 10"],
            ["010007", "MIZELL MEMORIAL HOSPITAL", "702 N MAIN ST", "OPP", "AL", "36467", "Covington", 0.867181, "7 out of 10"],
        ]

    def test_process_csv_stream_named_fields_success(self):
        csv_text = textwrap.dedent("""\
            Provider Number,Hospital Name,Address,City,State,ZIP Code
            010001,SOUTHEAST ALABAMA MEDICAL CENTER,1108 ROSS CLARK CIRCLE,DOTHAN,AL,36301
            010005,MARSHALL MEDICAL CENTER SOUTH,2505 U S HIGHWAY 431 NORTH,BOAZ,AL,35957
            010006,ELIZA COFFEE MEMORIAL HOSPITAL,205 MARENGO STREET,FLORENCE,AL,35631
            010007,MIZELL MEMORIAL HOSPITAL,702 N MAIN ST,OPP,AL,36467
            010011,ST VINCENT'S EAST,50 MEDICAL PARK EAST DRIVE,BIRMINGHAM,AL,35235
        """)
        csv_input_stream = io.StringIO(csv_text)

        results = self.csv_processor.process_csv_stream_named_fields(csv_input_stream)

        assert len(results) == 5
        assert results[0] == {"Provider Number": "010001", "Hospital Name": "SOUTHEAST ALABAMA MEDICAL CENTER",
                              "Address": "1108 ROSS CLARK CIRCLE", "City": "DOTHAN",
                              "State": "AL", "ZIP Code": "36301"}

        test = lambda rec: rec["Provider Number"] == "010006"
        eliza_coffee = next(filter(test, results), None)
        assert eliza_coffee["Hospital Name"] == "ELIZA COFFEE MEMORIAL HOSPITAL"
