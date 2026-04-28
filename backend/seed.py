import json
import requests

API_URL = "http://127.0.0.1:8000/figures/"
API_KEY = "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"

FIGURES = [
    {
        "name": "Julius Caesar",
        "era": -100,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Julius Caesar was a Roman general and statesman who played a critical role in the events that led to the demise of the Roman Republic and the rise of the Roman Empire. He conquered Gaul, crossed the Rubicon river in defiance of the Senate, and seized power in Rome. He implemented numerous reforms before being assassinated by a group of senators on the Ides of March 44 BC. Caesar was known for his clemency toward defeated enemies, but also for his absolute determination to maintain power."
    },
    {
        "name": "Cleopatra VII",
        "era": -69,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Cleopatra VII was the last active ruler of the Ptolemaic Kingdom of Egypt. She formed political alliances and romantic relationships with Roman leaders Julius Caesar and Mark Antony to maintain Egyptian independence. She was highly educated, speaking nine languages, and actively participated in political and military decisions. After the defeat at the Battle of Actium, rather than be captured by Octavian, she chose to end her own life."
    },
    {
        "name": "Genghis Khan",
        "era": 1162,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Genghis Khan was the founder and first Great Khan of the Mongol Empire. Born into a poor clan, he was abandoned as a child and fought his way to power through military alliances and conquest. He united the Mongol tribes through a combination of military force and political marriages. He created one of the largest empires in history through brutal military campaigns but also established religious tolerance and trade routes across Asia."
    },
    {
        "name": "Karl Marx",
        "era": 1818,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Karl Marx was a German philosopher and economist who developed the theory of communism. He spent his life in poverty, exiled from multiple countries for his revolutionary writings. He collaborated closely with Friedrich Engels and dedicated his life to analysing capitalism and advocating for the working class. He believed historical change came through class struggle and called for workers to unite against oppression."
    },
    {
        "name": "Harriet Tubman",
        "era": 1822,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Harriet Tubman was an American abolitionist and political activist. Born into slavery, she escaped and then made some thirteen missions to rescue approximately seventy enslaved people using the network of antislavery activists known as the Underground Railroad. She later served as a spy for the Union Army during the Civil War. Despite suffering a traumatic head injury as a child that caused narcoleptic episodes throughout her life, she never stopped fighting for freedom."
    }
]

def seed():
    for figure in FIGURES:
        # check if figure already exists
        check = requests.get(f"{API_URL}?name={figure['name']}")
        figure["api_key"] = API_KEY
        response = requests.post(API_URL, json=figure)
        ...

def seed():
    for figure in FIGURES:
        figure["api_key"] = API_KEY
        response = requests.post(API_URL, json=figure)
        if response.status_code == 200:
            print(f"Added: {figure['name']}")
        else:
            print(f"Failed: {figure['name']} - {response.text}")



if __name__ == "__main__":
    seed()