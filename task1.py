import pandas as pd
import matplotlib.pyplot as plt


def plot_sfd_bmd(excel_path: str="C:/Users/arnaw/Downloads/SFS_Screening_SFDBMD.xlsx", sheet_name: str = 'Sheet1'):
    """
    Plots the Shear Force Diagram (SFD) and Bending Moment Diagram (BMD)
    from an Excel sheet.

    Parameters:
        excel_path (str): Path to the Excel file.
        sheet_name (str): Sheet name containing the data (default is 'Sheet1').
    """
    # Read data
    df = pd.read_excel(excel_path, sheet_name='Sheet1')
    
    # Extract columns
    distance = df['Distance (m)']
    shear_force = df['SF (kN)']
    bending_moment = df['BM (kN-m)']

    # Create subplots for SFD and BMD
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot Shear Force Diagram (SFD)
    ax1.plot(distance, shear_force, color='blue', marker='o')
    ax1.set_title('Shear Force Diagram (SFD)')
    ax1.set_ylabel('Shear Force (kN)')
    ax1.grid(True)

    # Plot Bending Moment Diagram (BMD)
    ax2.plot(distance, bending_moment, color='red', marker='o')
    ax2.set_title('Bending Moment Diagram (BMD)')
    ax2.set_xlabel('Distance (m)')
    ax2.set_ylabel('Bending Moment (kN·m)')
    ax2.grid(True)

    # Adjust layout
    plt.tight_layout()
    plt.show()

    #Calling the function
print("Plotting started...")
plot_sfd_bmd()  
