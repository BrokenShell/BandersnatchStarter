from os import getenv
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    # Load environment variables from a .env file
    load_dotenv()

    # Connect to the MongoDB database using the provided URL and TLS certificate
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["bandersnatch"]

    def __init__(self, collection: str):
        """
        Initialize the Database class.

        Parameters:
        - collection (str): The name of the MongoDB collection.
        """
        self.collection = self.database[collection]

    def seed(self, amount: int) -> bool:
        """
        Seed the collection with monsters.

        Parameters:
        - amount (int): The number of monsters to seed. Default is 1000.

        Returns:
        - bool: True if the seeding was successful, False otherwise.
        """
        # Extract monsters from MonsterLab
        monsters = [Monster().to_dict() for _ in range(1, amount + 1)]

        # Insert monsters into the collection
        result = self.collection.insert_many(monsters)
        return result.acknowledged

    def reset(self):
        """
        Reset the collection by removing all documents.

        Returns:
        - bool: True if the reset was successful, False otherwise.
        """
        result = self.collection.delete_many({})
        return result.acknowledged

    def count(self) -> int:
        """
        Get the count of documents in the collection.

        Returns:
        - int: The number of documents in the collection.
        """
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """
        Retrieve data from the collection as a DataFrame.

        Returns:
        - DataFrame: A pandas DataFrame containing the collection data.
        """
        data = list(self.collection.find({}, {"_id": 0}))
        return DataFrame(data)

    def html_table(self) -> str:
        """
        Generate an HTML table representation of the collection data.

        Returns:
        - str: An HTML string representing the collection data as a table.
        """
        return self.dataframe().to_html()


if __name__ == '__main__':
    db = Database('bandersnatch')

    # Reset the collection, seed it with 1000 monsters, and print the count
    db.reset()
    db.seed(1000)
    print(db.count())

    # Print the DataFrame representation of the collection data
    print(db.dataframe())

    # Print the HTML table representation of the collection data
    print(db.html_table())


