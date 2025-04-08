# Vietnamese Crimes Laws News Summarization  

This project focuses on summarizing Vietnamese crime and law-related news articles by finetuned deep learning models: ViT5, MBart and MT5.  

## 📌 Features  
- Pre-trained deep learning models for text summarization.  
- Custom dataset processing crawl from VNExpress, Bao Phap Luat Viet Nam, Vietnamnet and training pipeline.  
- Support for both training from scratch and using pre-trained results.  

## 🚀 Getting Started  

### **Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/TRungtu041203/Vietnamese-Crimes-Laws-News-Summarization.git
   cd Vietnamese-Crimes-Laws-News-Summarization
Usage
1️⃣ Train a New Model

Run train/mbart.ipynb and train/ViT5.ipynb

2️⃣ Use Pre-Trained Model (Skip Training)

If you don’t want to train the model, you can use the pre-trained results available here:

📥 [Download Pre-Trained Models](https://drive.google.com/drive/folders/11pBnSqZgrUOnJRUEG78EQiTIMEGSCaAG)

Once downloaded, replace it in app.ipynb and run:

📂 Dataset
The dataset consists of crime and law-related news articles in Vietnamese. It is divided into:

- train.csv (Training Data)
- val.csv (Validation Data)
- test.csv (Testing Data)

🛠 Technologies Used
- Python
- TensorFlow / PyTorch
- Natural Language Processing (NLP)
- Deep Learning

📜 License

This project is open-source under the MIT License.

🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.
