---
title: Mark Chen 演講筆記
tags: [2024_Fall, Speech]
---
<!-- HackMD ID:cTzDIFZGTI2g_Y_Mr-njFQ -->  

# Mark Chen 演講 teaching GPTs to reason  

Nov 25, 2024  

MIT 畢業，去作 quant，然後加入 openai  

## history of scaling gpt  

* GPT-2, build model to solve one thing  
* GPT-3, inner and outer loop. Can generate news that fools human  
* GPT-4, perform well on exams(高中生). Scales predictably important for safety  

## Why reasoning  

沒有邏輯 (thinking) system 1 ok, system 2 bad  

## 方法  

### chain of thought  

給一些範例思考過程  
[Wei et al](https://arxiv.org/abs/2201.11903):甚至只需要叫 model think step by step(zero shot-few shot)  
**Insight**:  
* model 夠大(100B+)時才有效  
* 解決需要結構化思考的問題  
* 減少 "mental load per token"，我猜是指不用根據 token 背下答案，而是能有思考過程。像是數學應用題，不用背下題目對應的答案(記下每一個 a-b 等於多少)，而是拆解問題(問自己 a-b 應該是多少)。在應用題的情境中，ab pair 出現次數可能不夠讓模型學會，但是拆解成整數減法相對容易。  
* 從 pre-training 中的解釋、敘述，學到推理過程。  

[Wang et al](https://arxiv.org/abs/2203.11171): 試很多次 different reasoning paths，用最常見的答案  
solve ambiguous  

### tools+actions  

[Schick et al](https://arxiv.org/abs/2302.04761): 給模型用工具：用計算機、或是數字串有多少R。  
[Yao et al](https://arxiv.org/abs/2210.03629): ReAct。  

### sequential reasoning  

[Lightman et al](https://arxiv.org/abs/2305.20050): Let's verify step by step  
把問題拆成很多步驟，只把錯誤步驟挑出來，精準學習  

[Tao et al](https://arxiv.org/abs/2305.10601): Tree of thought，有時候思考會分枝，external checker。  
24 problem  
**Insight**:  
* search-based 的推論方法  
* 可結合 MCTS DFS BFS 等經典搜尋演算法  
* 可以用驗證來剪枝  
* 限制: 計算成本、搜尋方式很重要、搜尋空間可能太大  

### ChatGPT-o1  

[官網介紹](https://openai.com/index/learning-to-reason-with-llms/)  
PhD-level  
RL+CoT  
訓練越久或是跑的時候CoT想更久都可以得到更好的效果  
介紹官網上的 cipher task  
puzzgrid  

#### safety  

jailbreak更不容易，因為可以叫模型再想一想  
補充：剛剛找到一篇持反對觀點的XD [Shaikh et al](https://arxiv.org/abs/2212.08061)  


## QA  

台積電：問cost down問題。回答：讓模型更強，同時也在cost down，廢話  

zero shot CoT: separate knowledge from reasoning.  

8e7: 語言不一定是最好的知識與思考介質。答：確實語言是個限制，以後或許可以發展非語言。  

兩步驟（訓練、推論時CoT ToT）  
Agents。答：跟reasoning有很大關係  

未來用處：把它當一個PhD來用  
會讓使用者更笨或更聰明？答：smarter  