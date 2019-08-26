# webtoon_analysis
#df_comments['댓글']는 크롤링한 웹툰 댓글

df_comment = pd.DataFrame(columns=['댓글'])

df_comment['댓글'] = df_comments['댓글']
df_comment_list = df_comment.values.tolist()

web_tokens = [tokenize(row[0]) for row in df_comment_list]
print(web_tokens)


#model = gensim.models.Word2Vec(sentences=web_tokens,size=300,sg = 1, alpha=0.025,min_alpha=0.025, seed=1234,iter=20)
#model.build_vocab(web_tokens)
#model.train(web_tokens,total_examples=model.corpus_count,epochs = model.iter)

model = gensim.models.Word2Vec(sentences=web_tokens,size=100,sg = 0,window=5,min_count=0,workers=4 )
print("훈련 끝")
model.save('Word2vec.model')
model = Word2Vec.load('Word2vec.model')
print(model.wv.most_similar('진짜/Noun',topn=100))  ## topn = len(model.wv.vocab)
