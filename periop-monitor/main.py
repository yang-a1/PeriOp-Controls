# Entry point for the PeriOp Monitor application.

from app import PeriOpApp

# REQUIRES: This file must be executed directly as a script (e.g., "python3 main.py")
# MODIFIES: None
# EFFECTS: Launches the PeriOp Monitor GUI by creating an instance of PeriOpApp
#          and starting the Tkinter event loop with mainloop()
if __name__ == "__main__":
    # Create the main application instance and start the event loop
    app = PeriOpApp()
    app.mainloop()