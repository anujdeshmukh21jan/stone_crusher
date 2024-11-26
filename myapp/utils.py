import os
from datetime import datetime
from django.conf import settings
from jinja2 import Environment, FileSystemLoader
import pdfkit

import pdfkit
import cups


def modify_env_file(pairs_dict, env_file=".env"):
    """
    Modify the .env file by updating or adding multiple key-value pairs from a dictionary.

    :param pairs_dict: Dictionary containing key-value pairs to update in the .env file.
    :param env_file: The path to the .env file (default is '.env').
    """
    # Read the existing content from the .env file
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            lines = file.readlines()
    else:
        lines = []

    # Track the keys that have been updated
    updated_keys = set()

    # Go through each line and update the keys if found
    new_lines = []
    for line in lines:
        key_in_line = line.split("=")[0].strip()
        if key_in_line in pairs_dict:
            # If key exists in the dictionary, update its value
            new_lines.append(f"{key_in_line}={pairs_dict[key_in_line]}\n")
            updated_keys.add(key_in_line)
        else:
            new_lines.append(line)

    # Add any key-value pairs that were not found in the .env file
    for key, value in pairs_dict.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}\n")

    # Write the modified content back to the .env file
    with open(env_file, "w") as file:
        file.writelines(new_lines)


def generate_recipt(sale):
    try:
        
        
        # Prepare data for the receipt
        data = {
            "client_name": sale.client.name,
            "vehicle_number": sale.vehicle.registration_number,
            "driver_name": sale.driver,
            "weight_before_load": sale.vehicle.weight_capacity,
            "weight_after_load": sale.weight_after_load,
            "net_weight": sale.total_load_weight,
            "size_details": ", ".join(key for key, value in sale.size.items() if value is not None),
            "total_cost": sale.total_cost,
            "date": sale.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "bill_no": sale.id,
            "total_weight_tonnes":sale.total_load_weight_in_tonnes,
            "total_weight_brass":sale.total_load_weight_in_brass
            
        }
        breakpoint()

        # Render the receipt template
        html_content = render_template(
            os.path.join(settings.BASE_DIR, "templates", "reciept.html"),
            data,
        )
        if not html_content:
            print("Error: Unable to render receipt template.")
            return

        # Convert the rendered HTML to a PDF
        pdf_path = convert_html_to_pdf(html_content)
        if not pdf_path:
            print("Error: PDF generation failed.")
            return

        # Print the receipt
        print_receipt(pdf_path)

    except Exception as e:
        print(f"Error in generating receipt: {e}")


def convert_html_to_pdf(html_template):
    file_name = f"recipts/receipt.pdf"
    try:
        # Convert HTML string to PDF
        pdfkit.from_string(str(html_template), file_name)
        print(f"PDF file generated: {file_name}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

    return file_name


def render_template(template_name, data):
    try:
        file_loader = FileSystemLoader("/")
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        return template.render(data=data)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return None


def print_receipt(file_path):
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = list(printers.keys())[0]  # Use the first available printer
        conn.printFile(printer_name, file_path, "Receipt", {})
    except Exception as e:
        print(f"Error printing receipt: {e}")
