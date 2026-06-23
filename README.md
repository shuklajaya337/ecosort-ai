# EcoSort AI: Intelligent Waste Segregation Web Application 🌿

**EcoSort AI** is a full-stack, intelligent waste classification and segregation web application built to align waste disposal practices with the United Nations Sustainable Development Goals (**SDG 12: Responsible Consumption and Production**, **SDG 11: Sustainable Cities**, and **SDG 13: Climate Action**).

The application classifies waste items into 7 primary categories, recommends the correct disposal bin, indicates recyclability, and provides tailored environmental tips.

---

## 🛠️ Tech Stack & Key Libraries
* **Backend**: Python, Flask (Web Server & API endpoints)
* **Machine Learning**: Scikit-Learn (TF-IDF Vectorization, Multinomial Naive Bayes Model)
* **Data Processing**: Pandas (CSV Database loading and exact matching)
* **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism design, custom HSL theme tokens, dark/light toggle), Vanilla JavaScript (Asynchronous Fetch API, Live Autocomplete)

---

## 🌟 Key Features
* **Hybrid Detection Engine**: Checks a structured database (`dataset.csv`) for exact matches to guarantee 100% accuracy, falling back to a machine learning classifier for new/unseen items.
* **Typo-Tolerant AI**: Utilizes character-level n-gram features (sub-word analysis) to correctly identify items even with spelling mistakes or plural formatting (e.g., "plstic cups" ➔ Plastic Waste).
* **Live Search Autocomplete**: Queries the Flask backend dynamically in the background to provide instant matching suggestions as the user types.
* **Premium Responsive Dashboard**: Designed with glassmorphic cards, smooth fade-in transitions, and a local-storage persistent Dark/Light mode toggle.

---

## 📐 How it Works (System Architecture)
```text
                  [ User Input: "dirty soda can" ]
                                │
                                ▼
                     [ Flask Backend: app.py ]
                                │
             ┌──────────────────┴──────────────────┐
             ▼                                     ▼
      [ Database Search ]                 [ Machine Learning ]
       (dataset.csv Lookup)               (Multinomial Naive Bayes)
             │                                     │
      Matches Exactly? ──► YES ──► [Result]        │
             │                                     │
             NO ───────────────────────────► Predict Category
                                                   │
                                                   ▼
                                            [Predicted Result]
                                                   │
                                                   ▼
                                        [Color-Coded UI Display]
                                        (Bin recommendation + Eco Tips)
```

---

## ⚡ How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/shuklajaya337/ecosort-ai.git
   cd ecosort-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model:
   ```bash
   python train_model.py
   ```
4. Run the web server:
   ```bash
   python app.py
   ```
5. Open your browser and go to `http://127.0.0.1:5000/`.

---

## 🎓 Professional Learning Outcomes
This project demonstrates several production-level software development skills:
1. **Machine Learning Pipeline Design**: Combining feature extraction (`TfidfVectorizer`) and statistical classification (`MultinomialNB`) into a unified pipeline.
2. **Model Serialization**: Saving and loading trained classifiers using Python's `pickle` library.
3. **Asynchronous Web Communication**: Utilizing the Javascript `Fetch API` to query backend endpoints in the background without refreshing the page (AJAX/Single-Page Application concepts).
4. **Responsive UI/UX Engineering**: Developing cross-platform compatible layouts with flexible grids and modern aesthetic tokens.
