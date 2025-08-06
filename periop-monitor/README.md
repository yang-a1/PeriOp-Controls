# PeriOp Monitor

PeriOp Monitor is a custom-built GUI application developed using Python and Tkinter. It provides a visual interface for monitoring temperature data from a connected DHT22 sensor. The application is styled to mimic a medical panel, with interactive screens, real-time temperature display, and visual feedback through custom digit images.

---

## Features

- Home Screen:
  - Real-time temperature readout using image-based digits
  - Status panel and adjustable settings layout
  - Interactive stop/start button
- Monitor Mode Screen:
  - Graphical background with placeholders for future graphing
  - Access to Help screen (optional)
- Temperature readout pulled from physical DHT22 sensor (or simulated)
- Uses `.after()` loop for periodic updates
- Uses custom assets for all UI components

---

## Project Structure

