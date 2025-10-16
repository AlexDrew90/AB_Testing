import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter.font as tkfont
import pandas as pd

# Function to perform logistic regression

def run_logsitic_regression(df):
    import statsmodels.api as sm

    df['version'] = df['version'].astype('category')
    df['test_number'] = df['test_number'].astype('category')


    df['count_undesired_action'] = df['sample_size'] - df['count_desired_action']


    y = df[['count_desired_action','count_undesired_action']]
    X = pd.get_dummies(df[['test_number','version']], drop_first=True).astype(float)
    X = sm.add_constant(X)

    model = sm.GLM(
        endog=y, 
        exog=X, 
        family=sm.families.Binomial()
    )
    results = model.fit()
    return results


# Function to handle file selection and pass df to run_logistic_regression functoin
def select_file():
    
    # Ask the user to select the CSV file via file dialog
    file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        import numpy as np
        # Call the processing function and pass the file path and campaign name
        retrieved_df = pd.read_csv(file_path)
        results = run_logsitic_regression(retrieved_df)
        coef = results.params['version_B']
        pval = results.pvalues['version_B']
        odds_ratio = np.exp(coef)
        ci_low, ci_high = results.conf_int().loc['version_B']
        ci_low_or, ci_high_or = np.exp(ci_low), np.exp(ci_high)



        if pval <= 0.05:
            strength = "STRONG"
        elif pval <= 0.1:
            strength = "SUFFICIENT"
        else:
            strength = "INSUFFICIENT"

        if odds_ratio >= 1:
            line2 = f"People who saw version B were {odds_ratio:.2f}X as likely to perform the desired action as those who saw version A."
        else:
            line2 = f"People who saw version B were {1/odds_ratio:.2f}X less likely to perform the desired action than those who saw version A."

        line3 = f"The p-value is: {pval:.4f}. Brand & Marketing consider this {strength} evidence that the difference is statistically significant."

        line1 = f"(95% CI: {1/ci_high_or:.2f}–{1/ci_low_or:.2f})."
        # Display result in Tkinter popup
        message = f"{line1}\n\n{line2}\n\n{line3}"
        messagebox.showinfo("Combined A/B Test Results", message)

        
        # Close the main window after processing is done
        root.destroy()
    else:
        messagebox.showwarning("File Error", "No file selected!")


def download_example_csv(event=None):
    csv_content = """test_number,version,sample_size,count_desired_action
1,A,500,7
1,B,600,11
2,A,1500,21
2,B,1463,22
3,A,10000,100
3,B,9900,300
"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save Example CSV As",
        initialfile="required_format_example.csv"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(csv_content)

# Create the main GUI window
root = tk.Tk()
root.configure(bg='#EBE8E5')
root.title("Self-serve AB testing tool")

# make root's first cell expandable
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=0, sticky="nsew")


ttk.Label(
    frm,
    text=(
        "ABOUT"
        "\n\n"
        "This tool aims to provide the user with a method of combining the results of multiple A/B tests to increase the sample size (and therefore likelihood of acheiving a statistically significant result)."
        "\n\n"
        "The tool is platform agnostic, so it can used to combine A/B tests from emails/webpages/social media posts etc...(do not mix tests from different platforms)"
        "\n\n\n"
         "HOW TO USE"
        "\n\n"
        "After you have conducted multiple A/B tests (the control and variation the should be the same across each test). Arrange your data into the required format (example CSV file provided below)."
        "\n\n"
        'Finally, upload your results using the "Select CSV file" button and the tool will produce a report.'
    ),
    wraplength=400,  # maximum width in pixels before wrapping
    justify="left"
).grid(column=0, row=0, sticky="w", pady=(0,10))

# --- hyperlink-style label under the copy ---
link = tk.Label(frm, text="Download example CSV", fg="blue", cursor="hand2")
# underline the link text
link_font = tkfont.Font(link, link.cget("font"))
link_font.configure(underline=True)
link.configure(font=link_font)
link.grid(column=0, row=1, sticky="w", pady=(0, 12))
link.bind("<Button-1>", download_example_csv)

# (optional) hover feedback
def _hover_in(_): link.config(fg="#004aad")
def _hover_out(_): link.config(fg="blue")
link.bind("<Enter>", _hover_in)
link.bind("<Leave>", _hover_out)

# Button
select_file_button = tk.Button(
    frm, text="Select CSV File",
    command=select_file,
    bg='#001E62', fg='#fff', font=("bold", 10)
)
select_file_button.grid(row=2, column=0, pady=20, padx=20, sticky="w")

root.mainloop()
