import jieba
import sys
from collections import defaultdict
import linecache

postings = defaultdict(dict)
'''''''''
def getWords():
    f=open('./带标签短信.txt','r')
    outf=open('./带标签短信_seg.txt','a')
    stopwords = {}.fromkeys([ line.rstrip() for line in open('./stop_words.txt','r') ])
    lines=f.readlines()
    n=0
    for line in lines:
        segs=jieba.lcut(line.split('\t')[1].replace(' ','').strip())
        n+=1
        final = ''
        for i in range(len(segs)):
            seg = segs[i]
            if seg not in stopwords:
                final += seg
                final += ' '
        outf.write('%06d'%(n)+'\t'+final+'\n')
'''''''''
def getPostings():
    global postings
    f = open('./带标签短信_seg.txt','r')
    lines = f.readlines()  # 读取全部内容
    f.close()
    #i=0
    for line in lines:
        '''
        i+=1
        if i>10:
            break
        '''
        lline=line.strip().split('\t')
        if len(lline)>1:
            docid = lline[0]
            Slline=lline[1].split(' ')
            #print(lline)
            unique_terms = set(Slline)
            #print(unique_terms)
            for te in unique_terms:
                if te in postings.keys():
                    postings[te].append(docid)
                else:
                    postings[te] = [docid]

def getline(the_file_path, line_number):
  if line_number < 1:
    return ''
  for cur_line_number, line in enumerate(open(the_file_path, 'rU')):
    if cur_line_number == line_number-1:
      return line
  return ''

def show_answer(answer):
    if answer ==[]:
        print('No matched answers!')
    else:
        print('lengthOFanswers：', len(answer))
        for i in range(len(answer)):
            print(linecache.getline('./带标签短信.txt',int(answer[i])))


def merge2_and(term1, term2):
    global postings
    answer = []
    if (term1 not in postings) or (term2 not in postings):
        return answer
    else:
        i = len(postings[term1])
        j = len(postings[term2])
        x = 0
        y = 0
        while x < i and y < j:
            if postings[term1][x] == postings[term2][y]:
                answer.append(postings[term1][x])
                x += 1
                y += 1
            elif postings[term1][x] < postings[term2][y]:
                x += 1
            else:
                y += 1
        return answer


def merge2_or(term1, term2):
    answer = []
    if (term1 not in postings) and (term2 not in postings):
        answer = []
    elif term2 not in postings:
        answer = postings[term1]
    elif term1 not in postings:
        answer = postings[term2]
    else:
        answer = postings[term1]
        for item in postings[term2]:
            if item not in answer:
                answer.append(item)
    return answer


def merge2_not(term1, term2):
    answer = []
    if term1 not in postings:
        return answer
    elif term2 not in postings:
        answer = postings[term1]
        return answer

    else:
        answer = postings[term1]
        ANS = []
        for ter in answer:
            if ter not in postings[term2]:
                ANS.append(ter)
        return ANS


def merge3_and(term1, term2, term3):
    Answer = []
    if term3 not in postings:
        return Answer
    else:
        Answer = merge2_and(term1, term2)
        if Answer == []:
            return Answer
        ans = []
        i = len(Answer)
        j = len(postings[term3])
        x = 0
        y = 0
        while x < i and y < j:
            if Answer[x] == postings[term3][y]:
                ans.append(Answer[x])
                x += 1
                y += 1
            elif Answer[x] < postings[term3][y]:
                x += 1
            else:
                y += 1

        return ans


def merge3_or(term1, term2, term3):
    Answer = []
    Answer = merge2_or(term1, term2);
    if term3 not in postings:
        return Answer
    else:
        if Answer == []:
            Answer = postings[term3]
        else:
            for item in postings[term3]:
                if item not in Answer:
                    Answer.append(item)
        return Answer


def merge3_and_or(term1, term2, term3):
    Answer = []
    Answer = merge2_and(term1, term2)
    if term3 not in postings:
        return Answer
    else:
        if Answer == []:
            Answer = postings[term3]
            return Answer
        else:
            for item in postings[term3]:
                if item not in Answer:
                    Answer.append(item)
            return Answer


def merge3_or_and(term1, term2, term3):
    Answer = []
    Answer = merge2_or(term1, term2)
    if (term3 not in postings) or (Answer == []):
        return Answer
    else:
        ans = []
        i = len(Answer)
        j = len(postings[term3])
        x = 0
        y = 0
        while x < i and y < j:
            if Answer[x] == postings[term3][y]:
                ans.append(Answer[x])
                x += 1
                y += 1
            elif Answer[x] < postings[term3][y]:
                x += 1
            else:
                y += 1
        return ans

def do_rankSearch(terms):
    Answer = defaultdict(dict)
    for item in terms:
        if item in postings:
            for docid in postings[item]:
                if docid in Answer:
                    Answer[docid]+=1
                else:
                    Answer[docid] = 1
    Answer = sorted(Answer.items(),key = lambda asd:asd[1],reverse=True)
    return Answer

def do_search():
    choice=input("Please choose the type of search :\nboolean(b) or ranked(r) :")
    if choice.strip() is None:
        sys.exit()
    # 布尔查询
    if choice=='b':
        print('Query templates:\nA and/or B\nA and/or B and/or C')
        query = input("Search query >> :")
        if query=='\n':
            sys.exit()
        terms = query.strip().split(' ')
        #print(terms)
        # 搜索的结果答案
        if len(terms) == 3:
            # A and B
            if terms[1] == "and":
                answer = merge2_and(terms[0], terms[2])
                show_answer(answer)
            # A or B
            elif terms[1] == "or":
                answer = merge2_or(terms[0], terms[2])
                show_answer(answer)
            # A not B
            elif terms[1] == "not":
                answer = merge2_not(terms[0], terms[2])
                show_answer(answer)
            # 输入的三个词格式不对
            else:
                print("Input wrong!")

        elif len(terms) == 5:
            # A and B and C
            if (terms[1] == "and") and (terms[3] == "and"):
                answer = merge3_and(terms[0], terms[2], terms[4])
                show_answer(answer)
            # A or B or C
            elif (terms[1] == "or") and (terms[3] == "or"):
                answer = merge3_or(terms[0], terms[2], terms[4])
                show_answer(answer)
            # (A and B) or C
            elif (terms[1] == "and") and (terms[3] == "or"):
                answer = merge3_and_or(terms[0], terms[2], terms[4])
                show_answer(answer)
            # (A or B) and C
            elif (terms[1] == "or") and (terms[3] == "and"):
                answer = merge3_or_and(terms[0], terms[2], terms[4])
                show_answer(answer)
            else:
                print("Input wrong!")

        else:
            print("Input wrong OR More format is not supported now!")

    # 自然语言的排序查询，返回按相似度排序的最靠前的若干个结果
    elif choice=='r':
        print('Query template:\nA B C D...')
        query = input("Search query >> :")
        if query=='\n':
            sys.exit()
        terms = query.strip().split(' ')
        leng = len(terms)
        answer = do_rankSearch(terms)
        if answer ==[]:
            print('No matched answers!')
        else:
            #print("[Rank_Score: docid]")
            for (docid, score) in answer:
                print(str(score / leng) + ": " + str(docid)+'    '+linecache.getline('./带标签短信.txt',int(docid)))

    else:
        print("Input wrong!")

def main():
    #getWords()
    print('begin getPostings')
    getPostings()
    print('postings got')
    while True:
        do_search()


if __name__ == "__main__":
    main()
