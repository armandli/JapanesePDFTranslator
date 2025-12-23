import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import os
    import json
    from pathlib import Path
    from dotenv import load_dotenv
    from mistralai import Mistral, DocumentURLChunk

    from IPython.display import Markdown, display
    return (
        DocumentURLChunk,
        Markdown,
        Mistral,
        Path,
        display,
        json,
        load_dotenv,
        os,
    )


@app.cell
def _(load_dotenv):
    load_dotenv()
    return


@app.cell
def _(os):
    api_key = os.getenv("MISTRAL_API_KEY")
    return (api_key,)


@app.cell
def _(Mistral, api_key):
    client = Mistral(api_key=api_key)
    return (client,)


@app.cell
def _():
    data_dir = 'img/'
    return (data_dir,)


@app.cell
def _(Path, data_dir):
    files = [Path(data_dir + 'IMG_5CCBB5A69EE1-1.jpeg'), Path(data_dir + 'IMG_6CF3DC88D7D1-1.jpeg')]
    return (files,)


@app.cell
def _(files):
    files[0].stem
    return


@app.cell
def _(client, files):
    uploaded_files = [client.files.upload(file={"file_name": file.stem, "content": file.read_bytes()}, purpose="ocr") for file in files]
    return (uploaded_files,)


@app.cell
def _(client, uploaded_files):
    signed_urls = [client.files.get_signed_url(file_id=uploaded_file.id, expiry=1) for uploaded_file in uploaded_files]
    return (signed_urls,)


@app.cell
def _(DocumentURLChunk, client, signed_urls):
    ocr_responses = [client.ocr.process(document=DocumentURLChunk(document_url=signed_url.url), model='mistral-ocr-latest', include_image_base64=True) for signed_url in signed_urls]
    return (ocr_responses,)


@app.cell
def _(json, ocr_responses):
    response_dicts = [json.loads(ocr_response.model_dump_json()) for ocr_response in ocr_responses]
    return (response_dicts,)


@app.cell
def _(response_dicts):
    response_dicts
    return


@app.cell
def _(Markdown, display, response_dicts):
    for response_dict in response_dicts:
        for page in response_dict.get("pages", []):
            md = page.get("markdown", "")
            display(Markdown(md))
    return


@app.cell
def _():
    ### try segments
    return


@app.cell
def _(Path, data_dir):
    blockfiles = [
        Path(data_dir + 'block0_1.png'),
        Path(data_dir + 'block0_2.png'),
        Path(data_dir + 'block0_3.png'),
        Path(data_dir + 'block0_4.png'),
        Path(data_dir + 'block0_5.png'),
        Path(data_dir + 'block1_1.png'),
        Path(data_dir + 'block1_2.png'),
        Path(data_dir + 'block1_3.png'),
        Path(data_dir + 'block1_4.png'),
    ]
    return (blockfiles,)


@app.cell
def _(blockfiles, client):
    uploaded_blockfiles = [client.files.upload(file={"file_name": file.stem, "content": file.read_bytes()}, purpose="ocr") for file in blockfiles]
    return (uploaded_blockfiles,)


@app.cell
def _(client, uploaded_blockfiles):
    signed_blockurls = [client.files.get_signed_url(file_id=uploaded_file.id, expiry=1) for uploaded_file in uploaded_blockfiles]
    return (signed_blockurls,)


@app.cell
def _(DocumentURLChunk, client, signed_blockurls):
    ocr_responses2 = [client.ocr.process(document=DocumentURLChunk(document_url=signed_url.url), model='mistral-ocr-latest', include_image_base64=True) for signed_url in signed_blockurls]
    return (ocr_responses2,)


@app.cell
def _(json, ocr_responses2):
    response_dicts2 = [json.loads(ocr_response.model_dump_json()) for ocr_response in ocr_responses2]
    return (response_dicts2,)


@app.cell
def _(Markdown, display, response_dicts2):
    for response_dict2 in response_dicts2:
        for page2 in response_dict2.get("pages", []):
            md2 = page2.get("markdown", "")
            display(Markdown(md2))
    return


@app.cell
def _():
    page1 = """
    三人での研究

    木村が細川家を訪ねると、確かに伝書は 中山博道に渡すことになっていたと伝えら れており、何度も親族会議を開いた上での ことだが、木村に伝書を公開することにし た。
    その後、木村は一人で難解な伝書の解読 につとめ、あるいは新たな資料を収集し、参 想神樽重信流の全貌を著作にまとめる仕事 に精魂を傾けていく。
    やがて、木村の孤独な研究に関心を示す 強力な提案が現われる。橋本正武と猫田長、 ともに範士九段で中山博道との縁も深い居 合の大家である。
    橋本は中山の高弟で有信館幹事長を務めた橋本統陽を叔父にもち、東大農学部に通いながら有信館で中山に朔道を学んだ。早稲田大学で朔道の選手として活躍した額田は、三菱道場でその橋本統陽に居合を学んであり、戦後は大阪朔道界の重鎮であった。
    昭和46年、全日本居合道大会の場で、木村の話に動かされた二人は、木村の手助けをしながら、三人で額を寄せ合い、刀を握って技の研究を続ける。
    昭和49年、木村は夢想神傅重信流の講習会を防府で開いた。このとき額田長、橋本正武はもちろん、環量、紙本柔一、沖原功、永江又三郎といった当時の居合道界の重鎮たちが参加している。参加する人たちは起訴文を書いた。
    だが、この業の披露には反応はいま一つであったらしい。半年後にも研修会を開いたが、参加者は半数になった。しかし、木村、橋本、瀬田の三人は落胆することなく、研究を続ける。
    翌年には瀬田の本拠である大阪・堺の南海縁成館で研修会を行なった。これが防疫以外での初めての公開である。昭和52年には、日本武道館で開かれた第1回日本古武道大会で、瀬田と橋本が夢想神伝重信流と名乗って演武をしている。
    木村は夢想神傳重信流の伝書を一応写し終わったものの、本としての完成を見ずに、昭和53年に逝去した。その後を木村の息子茂喜と、額田、橋本が受け継ぐ。途中額田が健康を害し、最後は橋本と木村茂喜の共同作業で、膨大な伝書を現代文で解釈し、解説文、写真を付した『林崎抜刀術兵法 夢想神伝重信流傳書解説及び業手付解説』が上梓されたのは昭和57年のことだった。
    それから間もなく橋本、額田は病に倒れるが、額田の盟友であった西田英和（本年逝去）が会長となり、門人の尽力で昭和62年に夢想神傳重信流研究会が発足する。翌年には全日本剣道連盟主催の居合道講習会でも古流研究の時間に取り扱われた。
    その後紆余曲折はあったが、平成3年に夢想神傳重信流会と名称を改め、研修会、講習会を続けている。
    大阪、滋賀、茨城、京都、奈良、和歌山、福岡、石川など各地に門人がおり、近年左日本剣道演武大会でこの流名を名乗る人も増えている。2008年には14人を数えた。
    """

    page2 = """
    傅道の言い残したこと
    中山博道は「最後の武芸者」と呼ばれる通り、妥協のない姿勢で武術を追求した。そのため、居合の技についても、理合に合わない技は自分で改良し、年齢によって技が変わったともいわれる。
    自分の流儀についても、夢想神伝流と名乗ったのは戦前一度だけであり、没後になって四人たちが呼ぶようになったということには前項で紹介した。ある意味では現代におけるさまざまな混乱の元にもなっている。
    夢想神傳重信流も源は中山博道であり、その成立には複雑な事情がある。
    当時、土佐英信流は下村派、谷村派の二派に分かれていたが、中山博道は土佐の居合に深い関心を持ち、明治30年には高知へ赴いて谷村派の森本克久身らに学んだ。
    だが、中山の研究はそれに飽きたらず、その後、艱意だった板垣退助を通して下村派の細川義昌に入門した。他流と絶対混同しない、親兄弟にも言わない、見せないという起請文を書いての入門である。大正5年のことだった。
    そして大正12年に中山は細川に言伝を与えられたが、なぜか細川は伝書を渡さないままの年に亡くなった。しかし、「早く中山に伝書を渡さなければ」と展開まで言い残していたという。
    以上が従来の定説だが、実は不確かなところもあり、それを反証する資料も示されている。博道自身が下村派を名乗ったことはなく、門人たちに、自分が教えているのは五藤派（＝谷村派）の居合だと語っていたという証言がある。
    いずれにせよ、年月は不明だが、あるとき博道が門人である木村栄寿に「大正年間に義目から土佐英信派の奥義を授けられたが、その林崎甚助重信の技の伝書を受ける機会を逃した。いつかそれを写し、解読してほしい」と話したのが券恕神傅重信派の始まりである。
    つまり、中山博道が公に演武していたのは、ほとんどの場合に自ら名乗っていたように大森派や長谷川英信派の業であり（それが現在の券恕神伝流の原型となる）、細川から学んだ土佐英信派の奥義であり門外不出の居合、すなわち券恕神傅重信派は、そこに少しずつ取り入れていくつもりであったが、最後まで人間せずに没した、ということであるうか。
    山口県防府に生まれた木村は呉海兵団に入り、有信館呉支部などで中山に接し、大正8年に入門した。海軍を終えると武道家を志し、昭和2年、防府に剣道場を作る。中山が心信館と命名し、中山の道場有信館の防府支部となった。中山は西下すると数日返留し、木村を相手に枝の研鑽もしていた。研究熱心な木村を中山は信頼していたようだ。
    戦後、昭和33年に中山が没するが、49年前後から木村はその作業に一人取り組むことになる。
    """
    return


@app.cell
def _():
    translated_page1 = """
    Research by three people
    When Kimura visited the Hosokawa family, he was told that the document was indeed supposed to be given to Hiromichi Nakayama. After several family meetings, they decided to disclose the document to Kimura.
    Subsequently, Kimura devoted himself to deciphering difficult historical documents alone, collecting new materials, and pouring all his energy into compiling a comprehensive work that would reveal the complete picture of the Sanso Shintaru Shigenobu school of martial arts.
    Eventually, a powerful proposal emerged that showed interest in Kimura's solitary research. The proposal came from Masatake Hashimoto and Nagashi Nekota, both masters of iaido (Japanese sword drawing) with the rank of Hanshi 9th Dan, and both having close ties to Hiromichi Nakayama.
    Hashimoto was the nephew of Toyo Hashimoto, a senior disciple of Nakayama and the secretary-general of the Yushinkan dojo. While attending the University of Tokyo's Faculty of Agriculture, he studied Sakudo under Nakayama at the Yushinkan. Nukada, who was a successful Sakudo practitioner at Waseda University, studied iaido under Toyo Hashimoto at the Mitsubishi dojo and became a leading figure in the Osaka Sakudo community after the war.
    In 1971, at the All Japan Iaido Tournament, the two men were moved by Kimura's words, and together they assisted Kimura, putting their heads together, gripping their swords, and continuing their research into the techniques.
    In 1974, Kimura held a training seminar for the Muso Shinden Jushin-ryu style in Hofu.  At this time, prominent figures in the iaido world, including Nagatoshi Nukada and Masatake Hashimoto, as well as Tamaki Ryo, Juichi Kamimoto, Isao Okihara, and Matasaburo Nagae, participated.  The participants wrote a pledge of commitment.
    However, the reaction to this demonstration of their work was apparently not very positive.  They held another training session six months later, but the number of participants was halved.  Nevertheless, Kimura, Hashimoto, and Seta did not become discouraged and continued their research.
    The following year, a training session was held at the Nankai Enseikan in Sakai, Osaka, which was Seta's home base. This was the first public demonstration outside of disease prevention activities. In 1977, Seta and Hashimoto performed at the 1st Japan Kobudo Tournament held at the Nippon Budokan, under the name Muso Shinden Shigenobu-ryu.
    Although Kimura had completed copying the scrolls of the Muso Shinden Shigenobu-ryu school, he passed away in 1978 before the book was fully completed. His son, Shigeki Kimura, along with Nukada and Hashimoto, continued the work.  Nukada's health deteriorated along the way, and ultimately, through the collaborative efforts of Hashimoto and Shigeki Kimura, the voluminous scrolls were interpreted in modern Japanese, and a book titled "Hayashizaki Battōjutsu Hyōhō Musō Shinden Shigenobu-ryū Transmission Scrolls Commentary and Technique Explanation," complete with explanatory text and photographs, was finally published in 1982.
    Shortly thereafter, Hashimoto and Nukada fell ill, but Nukada's close friend, Hidekazu Nishida (who passed away this year), became chairman, and thanks to the efforts of their disciples, the Muso Shinden Shigenobu-ryu Research Association was established in 1987. The following year, it was also included in the classical martial arts research time at the Iaido training seminar organized by the All Japan Kendo Federation.
    Although there were various twists and turns along the way, the organization changed its name to Muso Shinden Shigenobu-ryu Association in 1991 and has continued to hold training sessions and workshops.
    There are disciples of this school in various locations, including Osaka, Shiga, Ibaraki, Kyoto, Nara, Wakayama, Fukuoka, and Ishikawa, and in recent years, the number of people using this school's name at the All Japan Kendo Demonstration Tournament has increased. In 2008, the number reached 14.
    """

    translated_page2 = """
    What Fu Dao left behind ???
    Hirokichi Nakayama, often called "the last true martial artist," pursued martial arts with an uncompromising attitude.  Because of this, he even modified iaido techniques that he felt didn't conform to sound principles, and it is said that his techniques changed as he aged.
    As for his own style, he only referred to it as Muso Shinden-ryu once before the war, and it was only after his death that four of his followers began using that name, as mentioned in the previous section. In a sense, this has become the source of various confusions in modern times.
    The Muso Shinden Ryu school of swordsmanship also originates from Nakayama Hakudo, and its establishment involved complex circumstances.
    At that time, the Tosa Eishin-ryu school was divided into two branches, the Shimomura branch and the Tanimura branch. Nakayama Hakudo had a deep interest in Tosa-style iaido and traveled to Kochi in 1897 to study under people like Morimoto Katsuhisa of the Tanimura branch.
    However, Nakayama's research did not stop there. He later sought out Itagaki Taisuke, a difficult man to approach, and through him, became a disciple of Hosokawa Yoshimasa of the Shimomura school.  His initiation involved writing a sworn oath promising never to mix their style with other schools, and never to speak of or demonstrate it to even his own family. This was in 1916 (Taisho 5).
    Then, in 1923, Nakayama received a message from Hosokawa, but for some reason, Hosokawa died that same year without handing over the written message. However, it is said that he left behind instructions, emphasizing, "I must give the message to Nakayama soon."
    The above is the conventional theory, but there are actually some uncertainties, and evidence contradicting it has also been presented. There is testimony that Hakudo himself never claimed to belong to the Shimomura school, and that he told his disciples that the iaido he was teaching was of the Goto school (which is the same as the Tanimura school).
    In any case, although the exact year is unknown, at some point Hiromichi told his disciple Eiju Kimura, "During the Taisho era, I received the secret teachings of the Tosa Eishin school from Yoshime, but I missed the opportunity to obtain the written transmission of the techniques of Jinsuke Shigenobu Hayashizaki. I want you to copy and decipher it someday." This marked the beginning of the Kenjo Shinden Shigenobu school.
    In other words, the techniques that Hiromichi Nakayama publicly demonstrated were, in most cases, those of the Omori school and the Hasegawa Eishin school, as he himself claimed (which formed the basis of the present-day Kenjutsu Shinden-ryu).  The secret techniques of the Tosa Eishin school, which he learned from Hosokawa and which were considered highly confidential and not to be taught outside the school, namely the Kenjutsu Shinden Jushin school, were something he intended to gradually incorporate, but he passed away before he could fully do so. Is that the correct interpretation?
    Kimura, born in Hofu, Yamaguchi Prefecture, joined the Kure Naval Corps and came into contact with Nakayama at places like the Yushinkan Kure branch, eventually becoming his disciple in 1919. After leaving the navy, he aspired to become a martial artist and built a kendo dojo in Hofu in 1927. Nakayama named it Shishinkan, and it became a branch of Nakayama's Yushinkan dojo in Hofu. When Nakayama traveled west, he would stay for several days, practicing and refining his techniques with Kimura. It seems that Nakayama trusted Kimura, who was very dedicated to his studies.
    After the war, Nakayama passed away in 1958, but from around 1949, Kimura continued the work alone.
    """
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
