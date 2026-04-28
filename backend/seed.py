import json
import requests

API_URL = "http://127.0.0.1:8000/figures/"
API_KEY = "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"

FIGURES = [
    {
        "name": "Hammurabi",
        "era": -1810,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Hammurabi was the sixth king of the First Babylonian dynasty. He created one of the earliest legal codes in history, the Code of Hammurabi, which established laws governing trade, property, and punishment. He personally reviewed legal cases and corresponded with governors across his empire. He expanded Babylon through military conquest while also building temples and irrigation systems for his people."
    },
    {
        "name": "Ramesses II",
        "era": -1303,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Ramesses II was the third pharaoh of the Nineteenth Dynasty of Egypt, often regarded as the greatest and most celebrated pharaoh of the Egyptian Empire. He led military campaigns into Canaan and Nubia and fought the Hittites at the Battle of Kadesh. Rather than admit defeat, he negotiated one of the earliest known peace treaties in history. He built more monuments and statues of himself than any other pharaoh."
    },
    {
        "name": "Qin Shi Huang",
        "era": -259,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Qin Shi Huang was the founder of the Qin dynasty and the first emperor of a unified China. He ended the Warring States period through military conquest and centralised power by abolishing feudalism. He standardised weights, measures, currency and writing across China. He built the Great Wall and a massive tomb guarded by the Terracotta Army. He burned books and buried scholars alive to suppress opposition."
    },
    {
        "name": "Confucius",
        "era": -551,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Confucius was a Chinese philosopher and politician of the Spring and Autumn period. He spent years travelling from state to state offering his services as an advisor, but was repeatedly rejected by rulers. He returned home and spent his final years teaching disciples and editing classical texts. He emphasised personal morality, social relationships, and justice, believing rulers should lead by moral example rather than force."
    },
    {
        "name": "Siddhartha Gautama",
        "era": -563,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Siddhartha Gautama was a monk, mendicant, sage and religious teacher who lived in ancient India. Born into a wealthy royal family, he abandoned his privileged life after encountering suffering in the world. He spent years as an ascetic before finding a middle path through meditation. He taught that suffering arises from desire and attachment, and that liberation comes through following the Eightfold Path."
    },
    {
        "name": "Socrates",
        "era": -470,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Socrates was a Greek philosopher credited as the founder of Western philosophy. He spent his life questioning Athenians about their beliefs through dialogue, exposing contradictions in their thinking. He was tried for impiety and corrupting the youth, and was sentenced to death. He refused to flee Athens or abandon his principles, choosing to drink hemlock rather than compromise his beliefs."
    },
    {
        "name": "Alexander the Great",
        "era": -356,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Alexander the Great was a king of the ancient Greek kingdom of Macedon who created one of the largest empires in history. He never lost a battle despite fighting vastly larger armies. He personally led charges in battle and was wounded multiple times. He spread Greek culture across Asia and Egypt, founding cities named after himself. His troops finally refused to march further east, forcing him to turn back."
    },
    {
        "name": "Han Wudi",
        "era": -156,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Han Wudi was the seventh emperor of the Han dynasty of China and one of its greatest rulers. He expanded the empire into Central Asia, Vietnam and Korea through military campaigns. He established the Silk Road trade routes and made Confucianism the official state philosophy. He centralised power by weakening aristocratic families and creating a civil service examination system."
    },
    {
        "name": "Augustus",
        "era": -63,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Augustus was the founder of the Roman Empire and its first emperor. After Julius Caesar's assassination, he outmanoeuvred rivals through political cunning rather than open warfare when possible. He transformed Rome from a republic into an empire while maintaining the appearance of republican institutions. He brought a long period of peace after decades of civil war and undertook massive building projects across the empire."
    },
    {
        "name": "Zhuge Liang",
        "era": 181,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Zhuge Liang was a Chinese statesman and military strategist who served as the Chancellor of Shu Han during the Three Kingdoms period. He was known for his exceptional intelligence and loyalty to the Liu Bei family. He invented military equipment including the repeating crossbow and land mines. Despite limited resources, he led multiple northern expeditions against the Wei kingdom, working himself to death in service of a cause he knew was likely lost."
    },
    {
        "name": "Muhammad",
        "era": 570,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Muhammad was the founder of Islam and regarded by Muslims as the messenger of God. Born an orphan in Mecca, he worked as a merchant before receiving his first revelation at age 40. He faced persecution in Mecca and fled to Medina, where he built a community of followers. He returned to conquer Mecca peacefully and united the warring Arab tribes under one faith before his death."
    },
    {
        "name": "Tang Taizong",
        "era": 598,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Tang Taizong was the second emperor of the Tang dynasty of China, widely considered one of the greatest emperors in Chinese history. He killed his brothers in a palace coup to secure the throne. Once emperor, he surrounded himself with capable advisors who were encouraged to criticise his decisions. He expanded the empire, reduced taxes, and promoted religious tolerance, creating a golden age of Chinese civilisation."
    },
    {
        "name": "Wu Zetian",
        "era": 624,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Wu Zetian was the only woman in Chinese history to assume the title of Empress Regnant. She entered the imperial court as a concubine and systematically eliminated rivals over decades to seize power. She expanded the civil service examination system to recruit talented officials regardless of birth. She crushed aristocratic opposition ruthlessly while also reducing taxes and improving conditions for peasants."
    },
    {
        "name": "Genghis Khan",
        "era": 1162,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Genghis Khan was the founder and first Great Khan of the Mongol Empire. Born into a poor clan and abandoned as a child, he fought his way to power through military alliances and conquest. He united the Mongol tribes and created the largest contiguous empire in history. He established religious tolerance and trade routes across Asia but his campaigns resulted in millions of deaths."
    },
    {
        "name": "Mansa Musa",
        "era": 1280,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Mansa Musa was the tenth Mansa of the Mali Empire, the wealthiest individual in human history by some estimates. He made a famous pilgrimage to Mecca in 1324 with a caravan of thousands of people and so much gold that he caused inflation across North Africa and the Middle East. He built mosques and universities across his empire and brought scholars back from his pilgrimage to develop education in Mali."
    },
    {
        "name": "Pachacuti",
        "era": 1418,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Pachacuti was the ninth Sapa Inca of the Kingdom of Cusco and the founder of the Inca Empire. He seized power from his father after leading a successful defence against an invading army his father had fled from. He transformed Cusco from a kingdom into a vast empire through military conquest and built Machu Picchu. He reorganised the entire Andean social and political structure and created the mit'a labour system."
    },
    {
        "name": "Moctezuma I",
        "era": 1398,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Moctezuma I was the fifth tlatoani of Tenochtitlan and considered the founder of the Aztec Empire. He expanded the empire through military conquest and established the system of tribute collection from conquered peoples. He built the great temple of Tenochtitlan and reorganised the social structure of Aztec society. He survived a major famine by distributing food reserves and reorganising agricultural production."
    },
    {
        "name": "Leonardo da Vinci",
        "era": 1452,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Leonardo da Vinci was an Italian polymath of the Renaissance who worked as a painter, engineer, scientist and inventor. He filled thousands of notebook pages with observations and designs for inventions centuries ahead of his time. He dissected human corpses to understand anatomy and designed flying machines, tanks and solar power. He left many works unfinished, constantly distracted by new ideas and curiosity."
    },
    {
        "name": "Suleiman the Magnificent",
        "era": 1494,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Suleiman the Magnificent was the tenth and longest-reigning Sultan of the Ottoman Empire. He personally led military campaigns into Europe, the Middle East and North Africa, expanding the empire to its greatest extent. He reformed the legal system and was known as a just ruler who could be approached by ordinary citizens with grievances. He was also a poet and goldsmith who patronised the arts and architecture."
    },
    {
        "name": "Akbar the Great",
        "era": 1542,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Akbar the Great was the third Mughal emperor who expanded and consolidated the empire across the Indian subcontinent. Despite being illiterate, he gathered scholars, artists and theologians at his court and listened to debates between different religions. He abolished the tax on non-Muslims and appointed Hindus to high government positions. He created a new syncretic religion called Din-i-Ilahi that attempted to unite different faiths."
    },
    {
        "name": "Galileo Galilei",
        "era": 1564,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Galileo Galilei was an Italian astronomer, physicist and engineer who played a major role in the Scientific Revolution. He improved the telescope and made astronomical observations that supported the heliocentric model of the solar system. He was put on trial by the Inquisition and forced to recant his findings. Under house arrest for the rest of his life, he continued his scientific work in secret."
    },
    {
        "name": "Isaac Newton",
        "era": 1643,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Isaac Newton was an English mathematician and physicist who is widely considered one of the most influential scientists of all time. He formulated the laws of motion and universal gravitation, developed calculus independently, and built the first practical reflecting telescope. He worked largely alone and was extremely secretive about his discoveries, sometimes waiting years before publishing. He spent more time on theology and alchemy than on physics."
    },
    {
        "name": "Kangxi Emperor",
        "era": 1654,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "The Kangxi Emperor was the fourth emperor of the Qing dynasty and one of China's longest-reigning emperors. He became emperor at age seven and personally took control of the government at fourteen by outmanoeuvring his regent. He suppressed the Revolt of the Three Feudatories, incorporated Taiwan into the empire, and negotiated the Treaty of Nerchinsk with Russia. He promoted Chinese culture while maintaining Manchu traditions."
    },
    {
        "name": "Peter the Great",
        "era": 1672,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "Peter the Great was a Russian tsar who transformed Russia into a major European power. He travelled incognito to Western Europe to learn shipbuilding and manufacturing techniques firsthand. He forced Russian nobles to adopt Western dress and customs. He founded Saint Petersburg as a European-style capital and built a modern navy from scratch. He executed his own son Alexei for conspiring against his reforms."
    },
    {
        "name": "George Washington",
        "era": 1732,
        "period": "ancient",
        "source": "Wikipedia",
        "raw_text": "George Washington was an American military officer and statesman who led the Continental Army to victory in the American Revolutionary War. He held the army together through devastating defeats and a brutal winter at Valley Forge. After becoming the first President of the United States, he voluntarily stepped down after two terms when he could have remained in power. He freed his enslaved people in his will."
    },
    {
        "name": "Napoleon Bonaparte",
        "era": 1769,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Napoleon Bonaparte was a French military commander who rose to prominence during the French Revolution and became Emperor of the French. He never lost a major battle for a decade, conquering most of Europe. He created the Napoleonic Code which formed the basis of civil law in many countries. After his final defeat at Waterloo, he was exiled to Saint Helena where he dictated his memoirs, carefully crafting his own historical legacy."
    },
    {
        "name": "Lin Zexu",
        "era": 1785,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Lin Zexu was a Chinese official of the Qing dynasty who is celebrated for his vigorous opposition to the opium trade. He confiscated and destroyed over a million kilograms of opium from British merchants without compensation. When Britain retaliated with military force in the First Opium War, he was made a scapegoat and exiled by the emperor. In exile, he continued to serve the empire and write about the need for modernisation."
    },
    {
        "name": "Simón Bolívar",
        "era": 1783,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Simón Bolívar was a Venezuelan military and political leader who led the independence of six South American nations from Spanish rule. Born into wealth, he gave up his comfortable life to lead military campaigns across the continent. He crossed the Andes with his army in conditions considered nearly impossible. He died poor and exiled, having liberated six nations but failed in his dream of a united South America."
    },
    {
        "name": "Abraham Lincoln",
        "era": 1809,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Abraham Lincoln was an American lawyer and statesman who served as the 16th President of the United States during the Civil War. Born in poverty, he educated himself by reading borrowed books by firelight. He held the Union together through the bloodiest war in American history and issued the Emancipation Proclamation to free enslaved people. He was assassinated just days after the war ended."
    },
    {
        "name": "Charles Darwin",
        "era": 1809,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Charles Darwin was an English naturalist who developed the theory of evolution by natural selection. He spent five years on the HMS Beagle voyage collecting specimens and observations. He spent over twenty years refining his theory before publishing On the Origin of Species, knowing the controversy it would cause. He continued working despite chronic illness and the death of his daughter, which shook his religious faith."
    },
    {
        "name": "Karl Marx",
        "era": 1818,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Karl Marx was a German philosopher and economist who developed the theory of communism. He spent his life in poverty, exiled from multiple countries for his revolutionary writings. He collaborated closely with Friedrich Engels and dedicated his life to analysing capitalism and advocating for the working class. He believed historical change came through class struggle and called for workers to unite against oppression."
    },
    {
        "name": "Meiji Emperor",
        "era": 1852,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "The Meiji Emperor was the 122nd Emperor of Japan who presided over a period of rapid industrialisation and modernisation known as the Meiji Restoration. Under his reign, Japan transformed from a feudal society to an industrialised nation within decades. He supported the abolition of the samurai class and the adoption of Western technology, legal systems and military organisation. Japan defeated China and Russia in wars during his reign."
    },
    {
        "name": "Thomas Edison",
        "era": 1847,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Thomas Edison was an American inventor who developed many devices that greatly influenced modern life. He created the phonograph, motion picture camera, and improved the electric light bulb. He established the first industrial research laboratory in Menlo Park, working with teams of researchers on systematic invention. He famously said he found ten thousand ways that did not work before finding the one that did."
    },
    {
        "name": "Sun Yat-sen",
        "era": 1866,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Sun Yat-sen was a Chinese revolutionary and statesman who played a fundamental role in the overthrow of the Qing dynasty. He spent years in exile raising funds and support for revolution while facing assassination attempts. He founded the Kuomintang political party and briefly served as the first provisional president of the Republic of China. He died before seeing China unified, still working on his Three Principles of the People."
    },
    {
        "name": "Nikola Tesla",
        "era": 1856,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Nikola Tesla was a Serbian-American inventor and electrical engineer who made crucial contributions to the development of alternating current electricity. He worked independently on visionary projects that were often dismissed by contemporaries. He lost a patent battle with Edison over electricity systems despite being technically correct. He died alone and poor in a hotel room, his later ideas largely ignored by the scientific establishment."
    },
    {
        "name": "Marie Curie",
        "era": 1867,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Marie Curie was a Polish-French physicist who conducted pioneering research on radioactivity. She was the first woman to win a Nobel Prize and the only person to win in two different sciences. Despite facing discrimination as a woman in science, she continued research in a leaking shed with minimal equipment. She died from aplastic anaemia caused by decades of radiation exposure from her own research."
    },
    {
        "name": "Mahatma Gandhi",
        "era": 1869,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Mahatma Gandhi was an Indian lawyer who led India's independence movement against British rule through nonviolent civil disobedience. He organised mass protests and fasted repeatedly to the point of near death. He was imprisoned multiple times and lived simply, spinning his own cloth to identify with the poorest Indians. He was assassinated shortly after achieving Indian independence."
    },
    {
        "name": "Lu Xun",
        "era": 1881,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Lu Xun was a Chinese writer considered the father of modern Chinese literature. He abandoned medicine after realising that curing physical illness was less important than curing the spiritual illness of Chinese society. He used sharp, satirical fiction to expose the hypocrisies of traditional Chinese culture and the suffering of ordinary people. He was constantly harassed by the Nationalist government and died in exile in Shanghai."
    },
    {
        "name": "Albert Einstein",
        "era": 1879,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity. He worked as a patent clerk when he published his most important papers. He fled Germany when the Nazis came to power and renounced his German citizenship. He later expressed deep regret about signing a letter encouraging the development of nuclear weapons. He spent his final years working alone on a unified field theory he never completed."
    },
    {
        "name": "Joseph Stalin",
        "era": 1878,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Joseph Stalin was the General Secretary of the Communist Party of the Soviet Union who became its dictator. Born into poverty, he became a revolutionary and was repeatedly imprisoned and exiled by the Tsar. After Lenin's death he outmanoeuvred rivals to seize total control. He industrialised the Soviet Union through forced collectivisation that caused millions to starve. He purged the Communist Party, military and society in waves of political terror."
    },
    {
        "name": "Winston Churchill",
        "era": 1874,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Winston Churchill was a British statesman who served as Prime Minister during World War Two. He refused to negotiate with Nazi Germany when Britain stood alone after the fall of France. His speeches and radio broadcasts sustained British morale during the Blitz. He was voted out of office in 1945 before the war was fully over. He wrote extensively throughout his life and won the Nobel Prize in Literature."
    },
    {
        "name": "Mao Zedong",
        "era": 1893,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Mao Zedong was a Chinese communist revolutionary who founded the People's Republic of China. He led the Communist Party through decades of civil war and the Long March. After founding the PRC, he launched the Great Leap Forward and Cultural Revolution, campaigns that resulted in millions of deaths. He maintained absolute political control until his death, eliminating rivals through purges."
    },
    {
        "name": "Alan Turing",
        "era": 1912,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Alan Turing was an English mathematician and computer scientist who is considered the father of theoretical computer science and artificial intelligence. He broke the German Enigma code during World War Two, contributing significantly to Allied victory. After the war he was prosecuted for homosexuality and subjected to chemical castration. He died two years later from cyanide poisoning, ruled a suicide, while working on mathematical biology."
    },
    {
        "name": "John F. Kennedy",
        "era": 1917,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "John F. Kennedy was the 35th President of the United States who navigated the Cuban Missile Crisis and established the Peace Corps. Despite chronic health problems he projected an image of youth and vitality. He committed the United States to landing a man on the Moon. He was assassinated in Dallas in 1963 before seeing most of his domestic agenda passed into law."
    },
    {
        "name": "Nelson Mandela",
        "era": 1918,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Nelson Mandela was a South African anti-apartheid activist who spent 27 years in prison for his opposition to the apartheid regime. Rather than becoming bitter, he emerged from prison preaching reconciliation. He became the first democratically elected President of South Africa and chose to serve only one term. He established the Truth and Reconciliation Commission to address past human rights abuses without triggering a cycle of revenge."
    },
    {
        "name": "Yuri Gagarin",
        "era": 1934,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Yuri Gagarin was a Soviet cosmonaut who became the first human to journey into outer space. Born into a peasant family, he became a military pilot before being selected for the space programme. He orbited the Earth once on April 12 1961 in a mission lasting 108 minutes. After his flight he became an international celebrity and advocate for space exploration before dying in a plane crash during a routine training flight."
    },
    {
        "name": "Deng Xiaoping",
        "era": 1904,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Deng Xiaoping was a Chinese communist revolutionary and statesman who led China through far-reaching market-economy reforms. He was purged three times during his political career, including during the Cultural Revolution, but always returned to power. He implemented the policy of reform and opening up that transformed China into the world's second largest economy. He maintained one-party rule while allowing economic freedom, suppressing the Tiananmen Square protests in 1989."
    },
    {
        "name": "Margaret Thatcher",
        "era": 1925,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Margaret Thatcher was the first female Prime Minister of the United Kingdom. Born above a grocer's shop, she studied chemistry before becoming a lawyer and politician. She broke the power of the trade unions, privatised state industries, and fought the Falklands War. She was known for never compromising on her principles, saying the lady is not for turning. She was eventually ousted by her own party after introducing the unpopular poll tax."
    },
    {
        "name": "Mikhail Gorbachev",
        "era": 1931,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Mikhail Gorbachev was the last leader of the Soviet Union who introduced the policies of glasnost and perestroika. He chose not to use military force to prevent Eastern European countries from leaving the Soviet sphere of influence. His reforms led to the dissolution of the Soviet Union, an outcome he did not intend. He accepted German reunification and received the Nobel Peace Prize, but was widely unpopular in Russia for the chaos that followed the Soviet collapse."
    },
    {
        "name": "Steve Jobs",
        "era": 1955,
        "period": "modern",
        "source": "Wikipedia",
        "raw_text": "Steve Jobs was an American entrepreneur who co-founded Apple and transformed multiple industries. He was forced out of Apple by his own board in 1985 but returned to save the company from bankruptcy. He launched the iMac, iPod, iPhone and iPad, insisting on perfect design even when it made products harder to engineer. He was known for his obsessive attention to detail and his ability to inspire people to achieve what they thought was impossible."
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