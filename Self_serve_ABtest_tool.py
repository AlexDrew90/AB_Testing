import tkinter as tk
from tkinter import filedialog, messagebox

# Function to perform logistic regression

def run_logsitic_regression(df):
    import pandas as pd
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
        import pandas as pd
        import numpy as np
        # Call the processing function and pass the file path and campaign name
        retrieved_df = pd.read_csv(file_path)
        results = run_logsitic_regression(retrieved_df)
        coef = results.params['version_B']
        pval = results.pvalues['version_B']
        odds_ratio = np.exp(coef)


        if pval <= 0.05:
            strength = "STRONG"
        elif pval <= 0.1:
            strength = "SUFFICIENT"
        else:
            strength = "INSUFFICIENT"

        if odds_ratio >= 1:
            line1 = f"People who saw version B were {odds_ratio:.2f}X as likely to perform the desired action as those who saw version A."
        else:
            line1 = f"People who saw version B were {1/odds_ratio:.2f}X less likely to perform the desired action than those who saw version A."

        line2 = f"The p-value is: {pval:.4f}. Brand & Marketing consider this {strength} evidence that the difference is statistically significant."
        # Display result in Tkinter popup
        message = f"{line1}\n\n{line2}"
        messagebox.showinfo("A/B Test Results", message)

        
        # Close the main window after processing is done
        root.destroy()
    else:
        messagebox.showwarning("File Error", "No file selected!")

# Create the main GUI window
root = tk.Tk()
root.configure(bg='#EBE8E5')
root.title("Self serve AB testing tool")

# Create and place the button for file selection
select_file_button = tk.Button(root, text="Select CSV File", command=select_file, bg='#001E62', fg='#fff', font=("bold", 10))
select_file_button.pack(pady=20, padx=20)

# Start the Tkinter event loop
root.mainloop()