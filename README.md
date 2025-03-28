# **Efficient Page Replacement Algorithm Simulator**  

## **Overview**  
The **Efficient Page Replacement Algorithm Simulator** is a Python-based tool that simulates and compares different page replacement algorithms used in operating systems. It helps visualize the behavior of **FIFO, LRU, and Optimal** algorithms in memory management.  

---

## **Features**  
- Implements **FIFO, LRU, and Optimal** page replacement strategies  
- Accepts **custom user input** for reference strings and frame count  
- Provides **step-by-step simulation** of page replacements  
- Displays **page fault counts** for each algorithm  
- Generates **graphical comparison** using Matplotlib  

---

## **Technologies Used**  
- **Python 3.12** – Core programming language  
- **Pandas** – For structured data handling  
- **Matplotlib** – For graphical representation  

---

## **Installation**  

### **Prerequisites**  
Ensure you have **Python 3.12** installed. Install dependencies using:  

```sh
pip install pandas matplotlib
```

### **Clone the Repository**  
```sh
git clone https://github.com/yourusername/page-replacement-simulator.git
cd page-replacement-simulator
```

---

## **Usage**  

### **Run the Simulator**  
Execute the script:  
```sh
python page_replacement.py
```

### **Input Example**  
```
Enter number of frames: 3
Enter reference string: 7 0 1 2 0 3 4 2 3 0 3 2
```

### **Sample Output**  
```
FIFO Page Faults: 9
LRU Page Faults: 7
Optimal Page Faults: 5
```
**A graph comparing page faults** will be displayed automatically.  

---

## **Future Enhancements**  
Add **LFU, Clock, and Second-Chance** algorithms  
Develop a **GUI-based simulator** using Tkinter  
Convert it into a **web-based tool**  

---

## **Contributing**  
Contributions are welcome!
1. **Fork the repository**
2. **Create a new branch**: `git checkout -b feature-new-algorithm`
3. **Commit your changes**: `git commit -m "Added LFU algorithm"`
4. **Push to the branch**: `git push origin feature-new-algorithm`
5. **Submit a pull request**

---

## **License**  
MIT License – Free to modify and distribute.  

---

## **Contact & Support**  
Found a bug? Open an issue or contact **pranav95515@gmail.com**  

If you like this project, consider **starring it on GitHub!**
