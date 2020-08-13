import pandas


anno_file_1 = ''
df_anno_1 = pandas.read_csv(anno_file_1,
                encoding='utf-8', sep='\t',
                names=['word', 'pinyin'],
                dtype={'word': str, 'pinyin': str})
anno_file_2 = ''
df_anno_2 = pandas.read_csv(anno_file_2,
                encoding='utf-8', sep='\t',
                names=['word', 'pinyin'],
                dtype={'word': str, 'pinyin': str})

ne = (df_anno_1 != df_anno_2).any(1)

print('Agreement: '+str(1-ne.sum()/len(ne)))