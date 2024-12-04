# 📄 Professional Invoice Creator

A powerful and flexible invoice generation tool that uses LaTeX for creating professional-looking PDF invoices with a modern PyQt-based user interface.

## ✨ Features

- 🎨 Professional PDF invoice generation using LaTeX
- 🔄 Flexible data input support (JSON, CSV)
- 🏢 Customizable company information and logos
- 💰 Automatic tax calculations
- 🎯 Project-specific invoice customization
- 🖥️ Modern dark-themed PyQt user interface

## 🛠️ Setup

1. Ensure you have Python installed
2. Install required dependencies:

   ```bash
   pip install pandas PyQt6 qdarktheme
   ```

## 📚 Usage

1. Configure your company information
2. Launch the UI:

   ```bash
   python qt_ui.py
   ```

3. Input invoice details through the user interface
4. Generate professional PDF invoices instantly

## 🗂️ Project Structure

- `Invoice_filler.py`: Core invoice generation logic
- `interface.py`: User interface implementation
- `renderer.py`: PDF rendering and LaTeX compilation
- `qt_ui.py`: PyQt application entry point
- `templates/`: LaTeX templates for invoices
- `ui/`: Qt Designer UI files
- `ui_elements/`: Generated PyQt UI classes
- `tools/UI_class_auto_gen.py`: UI file watcher and compiler
