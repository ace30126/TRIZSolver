# TRIZSolver

## Overview

TRIZSolver is a Python-based desktop application designed to assist users in creative problem-solving and idea generation. It leverages two powerful methodologies, TRIZ (Theory of Inventive Problem Solving) and SCAMPER, integrated with Google's Gemini AI to enhance and expand upon generated ideas. The application features a user-friendly interface built with CustomTkinter.

## Features

* Dual Idea Generation Modules:
    * TRIZ Module:
        * Utilizes the 39 Engineering Parameters and 40 Inventive Principles.
        * Implements a Contradiction Matrix to suggest relevant Inventive Principles based on user-defined improving and worsening features.
        * Loads Contradiction Matrix data flexibly from an external `triz_matrix.csv` file.
        * Provides detailed descriptions for each of the 40 Inventive Principles.
    * SCAMPER Module:
        * Guides users through the SCAMPER checklist (Substitute, Combine, Adapt, Modify/Magnify/Minify, Put to other uses, Eliminate, Reverse/Rearrange).
        * Presents guiding questions for each SCAMPER technique.
* Gemini AI Integration:
    * Connects to Google's Gemini API (requires a user-provided API key).
    * Uses Gemini's generative capabilities (with a high temperature setting for creativity) to:
        * Expand on ideas derived from selected TRIZ principles and user-defined problem contexts.
        * Generate novel ideas based on SCAMPER questions and user inputs.
* User-Friendly Interface:
    * Built with CustomTkinter for a modern and visually appealing GUI.
    * Intuitive navigation between TRIZ and SCAMPER modules.
* Convenience Features:
    * API Key Management: Allows users to save their Gemini API key in a `triz_solver_config.ini` file for automatic loading on subsequent uses.
    * Save Ideas: Enables users to save generated ideas (from both TRIZ and SCAMPER modules) to local text files.
    * In-App Help: Provides comprehensive help guides for both SCAMPER and TRIZ methodologies, explaining their concepts and usage within the application.
        * General help for SCAMPER and TRIZ.
        * Specific help for each SCAMPER technique.
        * Detailed descriptions for all 40 TRIZ Inventive Principles are displayed when a principle is selected.
* Modular Design: The codebase is structured into logical components (`main.py`, `ui_components.py`, `triz_core.py`, `scamper_core.py`, `gemini_client.py`) for better readability and maintainability.

## Technologies Used

* Python 3.x(3.13.3 windows 10 x64 at dev)
* CustomTkinter: For the graphical user interface.
* google-generativeai: Python SDK for interacting with the Gemini API.
* Standard Python Libraries: `configparser`, `os`, `datetime`, `csv`, `tkinter.filedialog`, `tkinter.messagebox`.

## Setup and Installation

Prerequisites:
* Python 3.7 or higher.
* `pip` (Python package installer).

Installation Steps (from source):

1.  Clone the repository (or download the source files):
    ```bash
    git clone https://github.com/ace30126/TRIZSolver.git
    cd TRIZSolver
    ```
2.  Install required Python packages:
    It's highly recommended to use a virtual environment.
    ```bash
    # Create a virtual environment (optional but recommended)
    python -m venv venv
    # Activate the virtual environment
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```
3.  Prepare Data Files:
    * Ensure `triz_matrix.csv` is present in the root directory of the project. This file should contain the 39x39 TRIZ Contradiction Matrix data. A template is provided in the repository, but it needs to be populated with actual TRIZ data for the TRIZ module to function effectively.
4.  Obtain a Gemini API Key:
    * You will need a valid API key from [Google AI Studio](https://aistudio.google.com/) (formerly MakerSuite) to use the Gemini-powered features.

## How to Use

1.  Run the application:
    Navigate to the project directory in your terminal and run:
    ```bash
    python main.py
    ```
2.  Enter Gemini API Key:
    * When the application starts, enter your Gemini API key in the "Gemini API Key" field at the top.
    * Click the "Save Key" button to store it in `triz_solver_config.ini` for future sessions. This step is only needed once, or when you want to change the key.
3.  Select a Mode (TRIZ or SCAMPER):
    * Click the "TRIZ" or "SCAMPER" button to open the respective module.
    * General help for each methodology is available via the "TRIZ Help" and "SCAMPER Help" buttons located in the top control bar.

### Using the SCAMPER Module

1.  Enter Item: Input the product, idea, or problem you want to analyze in the "Product/Idea/Problem to Analyze" field.
2.  Select SCAMPER Technique: Click on one of the SCAMPER techniques (e.g., "S (Substitute)") from the list on the left.
    * A "?" button next to the technique title in the right panel provides specific help for that technique.
3.  Review Questions & Input Your Ideas:
    * Guiding questions for the selected technique will be displayed.
    * Use the "My Ideas" textbox to jot down your initial thoughts based on these questions.
4.  Get Gemini Ideas: Click the "Gemini Ideas" button. The application will send your item, the selected SCAMPER technique, and your initial ideas (if any) to the Gemini API to generate more creative suggestions.
5.  Review & Save: The AI-generated ideas will appear in the "Gemini Suggested Ideas" textbox. You can then click "Save to File" to save these ideas to a local text file.

### Using the TRIZ Module

1.  Select Contradiction:
    * From the "Improving Feature" dropdown, select the engineering parameter you wish to improve.
    * From the "Worsening Feature" dropdown, select the engineering parameter that tends to degrade as a result of improving the first.
2.  Find Principles: Click the "Find Principles" button. The application will consult the `triz_matrix.csv` data to suggest relevant Inventive Principles for the selected contradiction.
3.  Review Suggested Principles:
    * The suggested principles will appear in the list on the left.
    * Click on any principle in this list to view its detailed description in the "Selected Principle Details" area on the right.
4.  Enter Problem Context: In the "Problem Context/Idea to Apply This Principle" textbox, describe the specific problem or idea you want to apply the selected TRIZ principle to. This context is crucial for Gemini to provide relevant suggestions.
5.  Get Gemini Ideas: Once a principle is selected and context is provided, click the "Gemini Ideas (Principle-based)" button. The application will use the selected TRIZ principle, its description, and your problem context to prompt the Gemini API for innovative solutions.
6.  Review & Save: The AI-generated ideas will appear in the "Gemini Suggested Ideas (TRIZ-based)" textbox. Click "Save to File" to save these ideas.

## Contributing

Contributions, issues, and feature requests are welcome! Please feel free to check the issues page or submit a pull request.

## License

This project is licensed under the MIT License. (You can choose to add an MIT License file or another license if you wish. If you do, create a `LICENSE` file and reference it here.)

---

*This README was generated with the assistance of an AI model.*
