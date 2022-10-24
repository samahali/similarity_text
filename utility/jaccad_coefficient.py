import pandas as pd


def read_single_col_in_dataset(key: str, file_path:str) -> list:
    """ This function used to read csv file and return a specific column after
     drop null values on it.
    Return:
        (list) items: It's contain all items for specific column on the csv.
    """
    df = pd.read_csv(file_path)
    items = df[key].dropna(axis=0)
    return list(items)


class TextSimilarity(object):
    """ This class is used for getting similarity scores and searching for similarities
    that are greater than a specific score"""
    def __init__(self, text, percentage):
        self.text = text
        self.percentage = percentage

    def text_similarity_score(self, text_to_compare: str) -> float:
        """ This method used The Jaccard similarity index (Jaccard similarity coefficient)
        compares members for two sets to see which members are shared and which are distinct.
        It's a measure of similarity between the two sets of data, with a range from 0% to 100%.
        The higher the percentage, the more similar the two populations are.
        we use here sets to get an intersection between two sets and a union for both sets then
        we divided the intersection of the similarity set with the union of two sets to get a score of them
        example: text_1 = hi everyone here
                 text_2 = hi everybody there
                 here we will find two sentences intersecting on the word "hi" so the intersection is 1
                 we need to divide it into the sets union and that will be "everyone here" + "hi" + "everybody there"
                 there summation of words in sets is 5 so 1/5 = 20%
        Args:
            (str) text_to_compare: this second sentences will be used to check similarity
        Return:
            (float) similarity_score: It's a measure of similarity in percentage
        """
        first_list = self.text.split(" ")
        second_list = text_to_compare.split(" ")
        similarity_intersection = len(set.intersection(*[set(first_list), set(second_list)]))
        union = len(set.union(*[set(first_list), set(second_list)]))
        similarity_score = round(float(similarity_intersection / union) * 100, 2)
        return similarity_score

    def search_for_similarity(self, texts: list[str]) -> list[dict]:
        """this method is used to fetch all texts that get a
        similarity matching greater than the similarity percentage we want to check

        Args:
            (list[str]) texts - contains a list of texts that we want to check for similarity with it
        Return:
            (list[dict]) similarity_score_list - contains matched texts and score of matching
        """
        similarity_score_list = []
        for text in texts:
            similarity_score = self.text_similarity_score(text)
            if similarity_score > self.percentage:
                similarity_score_list.append({"value": text, "score": similarity_score})
        return similarity_score_list
