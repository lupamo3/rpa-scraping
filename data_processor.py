import pandas as pd

def save_to_excel(news_data, filename="news_data.xlsx"):
    df = pd.DataFrame(news_data, columns=["Title", "Date", "Description", "Image URL", "Money Present"])
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    news_data = [
        (
            "Title 1",
            "2021-01-01",
            "Description 1",
            "https://example.com/image1.jpg",
            True
        ),
        (
            "Title 2",
            "2021-01-02",
            "Description 2",
            "https://example.com/image2.jpg",
            False
        )
    ]
    save_to_excel(news_data)