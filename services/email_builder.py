"""
email_builder.py

Coordinates the entire email generation process.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from services.config_loader import ConfigLoader
from services.excel_reader import ExcelReader

from extractors.audit_details import AuditDetailsExtractor
from extractors.observations import ObservationsExtractor
from extractors.score_table import ScoreTableExtractor

from services.table_html import TableHTMLBuilder
from templates.signatures import TATA_SIGNATURE

class EmailBuilder:

    def __init__(self, excel_file):

        self.excel_file = excel_file

        self.loader = ConfigLoader()

        self.config = self.loader.load("tata_capital")

        self.table_builder = TableHTMLBuilder()

    def build(self):

        # ---------------------------
        # Read Workbook
        # ---------------------------

        reader = ExcelReader(self.excel_file)

        reader.load()

        checklist = reader.get_checklist_sheet()

        score_sheet = reader.get_score_sheet()

        # ---------------------------
        # Extract Data
        # ---------------------------

        audit_details = AuditDetailsExtractor(
            checklist,
            self.config
        ).extract()

        observations = ObservationsExtractor(
            checklist,
            self.config
        ).extract()

        score_data = ScoreTableExtractor(
            score_sheet
        ).extract()

        score_table = score_data["rows"]
        score_summary = score_data["summary"]

        # ---------------------------
        # Generate HTML Tables
        # ---------------------------

        audit_html = self.table_builder.build_audit_table(
            audit_details
        )

        observation_html = self.table_builder.build_observations_table(
            observations
        )

        # Pass the complete score_data (rows + summary)
        score_html = self.table_builder.build_score_table(
            score_data
        )

        # ---------------------------
        # Load Email Template
        # ---------------------------

        env = Environment(
            loader=FileSystemLoader("templates")
        )

        template = env.get_template(
            "tata_email.html"
        )

        html = template.render(

            audit_date=audit_details.audit_date,

            auditor_name=audit_details.auditor_name,

            final_rating=score_summary["final_rating"],

            audit_details_table=audit_html,

            observations_table=observation_html,

            score_table=score_html

        )
        
        # Append email signature
        html += TATA_SIGNATURE

        subject = self.config["email"]["subject_format"].format(

            **{

                "Agency Name": audit_details.agency_name,

                "Agency Code": audit_details.agency_code

            }

        )

        return {

            "subject": subject,

            "audit_details": audit_details,

            "observations": observations,

            "score_table": score_table,

            "score_summary": score_summary,

            "html": html

        }