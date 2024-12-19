---
title: HTML 筆記
tags: [2024_Fall]
---
<!-- HackMD ID:7-7lrIZvQLKgEgcXTYsyIg -->  

HTML 筆記  
===  

HTML week 3  
===  

## Data labels  

### Supervised  

### Unsupervised  

### Semi-supervised  

### Self-supervised  

自己產生資料，比如從輸出產生輸入，把完整的拼圖打亂，叫Machine把它拼回去。  
[自監督式學習 Self-Supervised Learning for Computer Vision 之概述](https://medium.com/ching-i/%E8%87%AA%E7%9B%A3%E7%9D%A3%E5%BC%8F%E5%AD%B8%E7%BF%92-self-supervised-learning-for-computer-vision-%E4%B9%8B%E6%A6%82%E8%BF%B0-b0decf770abf)  

### Weakly-supervised  

### Reinforcement  

## Protocols  

### Batch  

### Online  

### Active  

## Input Spaces  

### Concrete  

### Raw  

### Abstract  

## Error  

[Where does the error come from?](https://wenwu53.com/where-does-the-error-come-from/)  

### No Free Lunch Theorem for Machine Learning  

Unseen cases可能與seen cases差異甚大  

### Off-Training-Set Error  

Test set太小則有可能與真實的正確率有偏差  
$E_{\text{out}}$：真實誤差  
$E_{\text{in}}$：根據seen cases得到的誤差  
用[Hoeffding’s Inequality](https://en.wikipedia.org/wiki/Hoeffding%27s_inequality) bound兩者的誤差。  
$$ \begin{align*} &\Pr_{\mathcal{D}}[\mathcal{D}\text{ is bad}]\\  
=&\Pr_{\mathcal{D}}[\mathcal{D}\text{ is bad for }h_1\lor\mathcal{D}\text{ is bad for }h_2\lor\cdots\lor\mathcal{D}\text{ is bad for }h_M]\\  
\le&\Pr_{\mathcal{D}}[\mathcal{D}\text{ is bad for }h_1]+\Pr_{\mathcal{D}}[\mathcal{D}\text{ is bad for }h_2]+\cdots+\Pr_{\mathcal{D}}[\mathcal{D}\text{ is bad for }h_M]\\  
\le&2M exp(-2\epsilon^2N)  
\end{align*}  
$$  

>$|\mathcal{H}|$的大小：  
>太大：bound太大，$E_{\text{out}}$和$E_{\text{in}}$可能差很大  
>太小：找不到好的$h\in\mathcal{H}$使得$E_{\text{in}}$很小  
>  
>但是PLA的$|\mathcal{H}|=\infty$怎麼辦？  

abbr: PAC=probably approximately correct  

HTML week 4  
===  

bound the distance between $E_in$ and $E_out$ by the number of hypotheses. but for infinite hypotheses? Classify them into dichotomies(from parameters to the classification results of samples). In a binary classification problem, the number of dichotomies is upper bound by $2^N$ where N is the number of samples. growth function: the maximum number of dichotomies among possible inputs(to make it independent of inputs), denoted as $m_{\mathcal{H}}(N)$. But for some tasks, the number of dichotomies may be lower,  
* 1D perceptron, $f(x)=sign(x-h)$, $m_{\mathcal{H}}(N)=N+1$,bp:2  
* positive intervals(1D), $f(x)=1$ if $x\in [l,r),\ 0$ otherwise, $m_{\mathcal{H}}(N)=\binom{N+1}{2}+1=\frac{1}{2}N^2+\frac{1}{2}N+1$, bp:3  
* Convex sets(2D), 用凸的圖形把一個分類包起來，$m_{\mathcal{H}}(N)=2^N$, bp:no  
* 2D perceptron, $m_{\mathcal{H}}(N)<2^N$ in some cases, bp:4  

$k$ is a breakpoint if $m_{\mathcal{H}}(k)<2^k$, property: all $n>$minimum break point are break points.  
For some N, k inputs can be shattered by $\mathcal{H}\Leftrightarrow\ m_{\mathcal{H}}(N)=2^N$  
For a set of hypotheses for a task, VC dimension=breakpoint-1, VC dimension means the last $n$ s.t. the hypotheses can shatter any possible N inputs. VC dimension can be view as the strength of a set of hypotheses.  

It's proven that for $N\ge 2, k\ge 3$, $m_{\mathcal{H}}(N)\le N^{k-1}$  

HTML week 5  
===  

## Error functions are application/user-dependent.  
Example:  
* In a supermarket fingerprint verification system that verifies customers and collects points for discounts, false rejection is a serious problem.  
* In the CIA, false acceptance will be *VERY* serious because we let intruders in.  

HTML week 6  
===  

linear classification: h(x)=sign(s), error: 0/1  
linear regression: h(x)=s, error: mse  
logistic regression: h(x)=$\theta(s)$, error: cross-entropy  

non-linear transform + linear model => non-linear model  

HTML week 7  
===  

## Introduce overfitting  

low $E_{\text{in}}$, high $E_{\text{out}}$  

## Causes of overfitting  

* too much noise but too few samples  
* too complex target but too few samples  
* too complex model(large $d_{vc}$) for simple target but very few samples.  

## Avoid Overfitting  

* start from simple models  
* data cleaning/pruning  
* data hinting  
* regularization  
* Validation  

### Data cleaning/pruning  

Maybe automatically detect outliers, and  
* data cleaning: correct the label  
* data pruning: remove the sample  
the effect may be limited  

### data hinting  

Example: slightly shift/rotate images to generate more data.  
Aka data augmentation  

HTML week 8  
===  

## validation  

validation set：作弊，$\mathcal{D}\to\mathcal{D}_{train}\cup\mathcal{D}_{val}$從training data分$K$個出來當作選擇hypothesis的標準。  
$$  
E_{\text{out}}(g)\underset{small\ K}\approx E_{\text{out}}(g^-)\underset{large\ K}\approx E_{\text{val}}(g^-)  
$$  
practical: $\frac{K}{N}=20\%$  

## Cross Validation  

### Single Cross Validation  

$K=1$  
When choose n-th data as validation set, $E_{\text{val}}=e_n$  

#### leave-one-out cross-validation estimate  

$E_{loocv}(\mathcal{H},\mathcal{A})=\frac{1}{N}\sum_{n=1}^N e_n$  
Hope $E_{loocv}(\mathcal{H},\mathcal{A})\approx E_{\text{out}}(g)$  
$$  
\mathbb{E}_{\mathcal{D}} E_{loocv}(\mathcal{H},\mathcal{A})=\mathbb{E}_{\mathcal{D}}\frac{1}{N}\sum_{n=1}^N e_n=\overline{E_{\text{out}}}(N-1)  
$$  

#### disadvantage  

It takes a lot of time. Not practical.  

### V-fold Cross Validation  

把資料切成V份，輪流把其中一份當作validation。  
practical: $V=5\sim 10$  

### Don't fool yourself  

Report test result instead of best validation result.  

## Three principles  

### 奧坎剃刀(Occam's Razor)  

越簡單越好。  
只加入必要的東西。  

### Sampling Bias  

**Machine learning may cause harm.**  

#### Story  

* 選舉民調：手機太貴，某一黨的支持者比較買得起，因此有誤差  
* Netflix competition：validation error: **13%** improvement :rocket: :rocket: :rocket:  
**BUT** validation: **random examples** within $\mathcal{D}$  
test: **last** user records **after** $\mathcal{D}$  

HTML week 9  
===  

#### Solution  

**Match test scenario as much as possible**  
One possible solution: emphasize later samples  

##### Bank credit card approval problem  

* 時間偏差  
金融市場會改變，比如通貨膨脹、貨幣流通量改變  
* 分布偏差  
    * 要核准信用卡後觀察一段時間才能決定，有可能被拒絕的人其實是個好客戶（distribution不同，一個是所有人、一個是只包含以前核准過的客戶）  
    * 也許以前的年輕人信用狀況都不好，之後的年輕人可能就難以核准  

### Data Snooping  

If designing the model while snooping(偷看) data, it may overfit.  
If a data set has affected any step in the learning process, its ability to assess the outcome has been compromised.  

* 偷看test data，並照資料做model，失去test data獨立的作用。像是投信調參數做出過去績效很好的指數來發行ETF，但是未來表現未必好。  
* Data reusing: 每次都看以前的論文，做得更好才發表。一直對data做某件事，可能就會變相的在偷看測試資料。  

#### secret solution  

carefully balance between data-driven modeling(snooping) and validation (no-snooping)  

## Linear Support Vector Machine  

### Fatness for a model solving linearly separable data  

> If many hypotheses can perfectly solve this, choose the one with the largest "Robustness"(can classify even if some test data is affected by noise.)  

Robustness = Fatness of saparating hyperplane = the distance to the nearest $x_n$(margin).  
Choose the one with the largest margin and can perfectly separate data.  

### Distance to Hyperplane  

Shorten x and w first. Make $x=(x_0(=1),\ldots,x_n)$ -> $x=(x_1,\ldots,x_n)$, and $w=(w_0,\ldots,w_n)$ -> $w=(w_1,\ldots,w_n)$ and $b(=w_0)$.  
So $h(x)=w^Tx$ -> $h(x)=w^Tx+b$  
Want to know the distance(x,b,w) = the distance between x and hyperplane $w^Tx'+b=0$  
distance=project some $(x-x')$ to orthogonal of the hyperplane(the normal vector $w$)=$|\frac{w^T(x-x')}{\|w\|}|=\frac{1}{\|w\|}|w^Tx+b|$  

### Support Vector Machine  

* Saparating: for every n, $y_n(w^Tx_n+b)>0$  
* distance $=\frac{1}{\|w\|}y_n(w^Tx+b)$  

Goal: Find $argmax_{b,w} \frac{1}{\|w\|}$ subject to $\min_{n} y_n(w^Tx+b)=1$  

> If $\min_{n} y_n(w^Tx+b)>1$, say $1.127$, we can let $b'=\frac{b}{1.127}, w'=\frac{w}{1.127}$ so that $\frac{1}{\|w\|}$ is larger.  

Origin of name: The optimal boundary only depends on the nearest points(support vectors(candidates)).  

#### Solve with QP(Quadratic Programming)  

It's equivalent to finding the minimum of $\frac{1}{2}w^Tw$. And minimum of $\frac{1}{2}u^TQu+p^Tu$ subject to $a_m^Tu\ge c_m$ for $m=1,\ldots,M$,  
where  
$$  
u=\begin{bmatrix}  
b\\  
w  
\end{bmatrix};Q=\begin{bmatrix}  
0 & 0_d^T\\  
0_d & I_d  
\end{bmatrix};p=0_{d+1}  
$$  
$$  
a_n^T=y_n\begin{bmatrix}  
1 & x_n^T  
\end{bmatrix};c_m=1;M=N  
$$  
easy with QP solver $u\gets QP(Q,p,A,c)$  

### With non-linear transform  

可以像Linear model一樣直接把transform後的資料作為輸入跑Linear SVM，但因為有些transform後的維度($\tilde{d}$)非常大，像是d維資料的Q-order polynomial transform $\Phi_Q$的$\tilde{d}=O(Q^d)$，$Q=10,d=12$就會爆炸，因此depend on $\tilde{d}$ 不利於使用更複雜的transform，要使用對偶來消除  

HTML week 10  
===  
## Dual Support Vector Machine  

如上所述，(Non-)Linear SVM要optimize $\tilde{d}+1$ 個variables($\textbf{w}$和b)，且符合$N$個條件($y_n(\textbf{w}^T\textbf{z}_n+b)\ge 1$，即每一筆資料都正確分類)。  
We want to construct an equivalent SVM with $N$ variables and $N+1$ constraints. 細節需要太多的數學過程，因此只介紹必要部分。  

### Tool: Lagrange Multipliers  

> #### 以regularization舉例  
> $\min_{\textbf{w}}E_{\text{in}}(\textbf{w})$ s.t. $\textbf{w}^T\textbf{w}\le C$$\iff$$\min_{\textbf{w}}E_{aug}(\textbf{w})=E_{\text{in}}(\textbf{w})+\frac{\lambda}{N}\textbf{w}^T\textbf{w}$  
> 如果想要讓weight length $\le C$，相當於給定另一個參數$\lambda$。  

#### Constrained to Unconstrained  

用Lagrange Multipliers把原本$\min_{b,\textbf{w}}\frac{1}{2}\textbf{w}^T\textbf{w}$ s.t. $\forall n,y_n(\textbf{w}^T\textbf{z}_n+b)\ge 1$ 變成 $\mathcal{L}(b,\textbf{w},\vec\alpha)=\frac{1}{2}\textbf{w}^T\textbf{w}+\sum_{n=1}^N \alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n+b))$  
其中$all\ \alpha_n\ge 0$，KKT會用到。  

##### Claim  

$$  
\begin{align*}  
&\text{SVM 相當於}\min_{b,\textbf{w}}\left(\max_{all\ \alpha_n\ge 0}\mathcal{L}(b,\textbf{w},\vec\alpha)\right)\\  
=&\min_{b,\textbf{w}}\left(\infty\text{ if violate};\frac{1}{2}\textbf{w}^T\textbf{w}\text{ if feasible}\right)  
\end{align*}  
$$  
> violate, feasible: Does $(b,\textbf{w})$ satisfy constraints?  

##### Proof of Claim  

* For violating $(b,\textbf{w})$，then some $(1-y_n(\textbf{w}^T\textbf{z}_n+b)$ is positive, maximizing $\mathcal{L}$ will let corresponding $\alpha_n=\infty$, so the result is $\infty$ too.  
* For feasible $(b,\textbf{w})$, all $(1-y_n(\textbf{w}^T\textbf{z}_n+b)\le 0$. Since $all\ \alpha_n\ge 0$, the maximum of the second term(summation)=0, so maximum $\mathcal{L}=\frac{1}{2}\textbf{w}^T\textbf{w}$  

### Lagrange Dual Problem  

For any fixed $\vec\alpha'$ with all $\alpha'_n\ge 0$,  
$$  
\min_{b,\textbf{w}}\left(\max_{all\ \alpha_n\ge 0}\mathcal{L}(b,\textbf{w},\vec\alpha)\right)\ge \min_{b,\textbf{w}}\mathcal{L}(b,\textbf{w},\vec\alpha')  
$$  
Because max $\vec\alpha>$ any $\vec\alpha'$, and this still holds after $\min_{b,\textbf{w}}$.  
For the best $\vec\alpha'$, the above also holds, so  
$$  
\min_{b,\textbf{w}}\left(\max_{all\ \alpha_n\ge 0}\mathcal{L}(b,\textbf{w},\vec\alpha)\right)\ge \max_{all\ \alpha'_n\ge 0}\left(\min_{b,\textbf{w}}\mathcal{L}(b,\textbf{w},\vec\alpha')\right)  
$$  
LHS is equivalent to the original SVM, called primal. RHS is called Lagrange dual.  

### Strong/weak Duality of QP  

In the Lagrange dual problem,  
* $\ge$: weak duality  
* $=$: strong duality, when  
    * convex primal  
    * feasible primal($\Phi$-separable(after transform))  
    * linear constraints  

Strong duality means there exists a primal-dual optimal solution for both sides.  

### Solving  

#### eliminate b  

Since inner $\min_{b,\textbf{w}}$ has no constraints on $\vec\alpha$ (unconstrained), we can simply take a partial derivative on $b$.  
$$  
\begin{align*}  
&\mathcal{L}(b,\textbf{w},\vec\alpha)=\frac{1}{2}\textbf{w}^T\textbf{w}+\sum_{n=1}^N \alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n+b))\\  
&\frac{\partial \mathcal{L}(b,\textbf{w},\vec\alpha)}{\partial b}=0=-\sum_{n=1}^N \alpha_ny_n  
\end{align*}  
$$  
If we want to maximize $\mathcal{L}(b,\textbf{w},\vec\alpha)$, we can set(without loss of optimality) the constraint $\sum_{n=1}^N \alpha_ny_n=0$  
Therefore, we can remove b:  

$$  
\begin{align*}  
&\min_{b,\textbf{w}}\frac{1}{2}\textbf{w}^T\textbf{w}+\sum_{n=1}^N \alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n+b)\\  
&\min_{b,\textbf{w}}\frac{1}{2}\textbf{w}^T\textbf{w}+\sum_{n=1}^N \alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n))-b\sum_{n=1}^N \alpha_ny_n  
\end{align*}  
$$  
Under a constraint outside $\min$, $\sum_{n=1}^N \alpha_ny_n=0$.  
Since the last term is $0$.  

#### find w  

Similarly, we can simply take a partial derivative on $\textbf{w}$.  
$$  
\begin{align*}  
&\mathcal{L}(b,\textbf{w},\vec\alpha)=\frac{1}{2}\textbf{w}^T\textbf{w}+\sum_{n=1}^N \alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n+b))\\  
&\frac{\partial \mathcal{L}(b,\textbf{w},\vec\alpha)}{\partial w_i}=0=w_i-\sum_{n=1}^N \alpha_ny_nz_{n,i}  
\end{align*}  
$$  
We then have $\textbf{w}=\sum_{n=1}^N \alpha_ny_n\textbf{z}_n$  
Then substitute it into the expression:  
$$  
\begin{align*}  
&\max_{all\ \alpha_n\ge 0}\left(\min_{b,\textbf{w}}\frac{1}{2}\textbf{w}^T\textbf{w}+\sum_{n=1}^N \alpha_n-\textbf{w}^T\textbf{w}\right)\\  
&\max_{all\ \alpha_n\ge 0}\left(-\frac{1}{2}\left\|\sum_{n=1}^N \alpha_ny_n\textbf{z}_n\right\|^2+\sum_{n=1}^N \alpha_n\right)  
\end{align*}  
$$  
Under addtional constraints for $\max$: $\sum_{n=1}^N \alpha_ny_n=0$ and $\textbf{w}=\sum_{n=1}^N \alpha_ny_n\textbf{z}_n$.  

### KKT condition  

If $(b,\textbf{w},\vec\alpha)$ is a optimal solution for Lagrange dual, and  
* 原本的問題有解， primal feasible:  
$y_n(\textbf{w}^T\textbf{z}_n+b)\ge 1$  
* 滿足Dual的條件， dual feasible:  
$\alpha_n\ge 0$  
* 滿足Dual的最佳化條件，因此內部是optimal，dual-inner optimal:  
$\sum_{n=1}^N \alpha_ny_n=0$ and $\textbf{w}=\sum_{n=1}^N \alpha_ny_n\textbf{z}_n$  
* 滿足原本問題的最佳化條件，因此所有Lagrange terms消失，primal-inner optimal:  
$\alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n+b))=0$  

Called Karush-Kuhn-Tucker (KKT) conditions  

### 小結  

根據以上結論，我們可以用QP解  
$$  
\min_{all\ \alpha_n\ge 0}\left(\frac{1}{2}\left\|\sum_{n=1}^N \alpha_ny_n\textbf{z}_n\right\|^2-\sum_{n=1}^N \alpha_n\right)  
$$  
得出 $\vec\alpha$，再用以上條件得出 $b,\textbf{w}$  

#### w  

optimal $\vec\alpha\Rightarrow$ optimal $\textbf{w}=\sum_{n=1}^N \alpha_ny_n\textbf{z}_n$  

#### b  

optimal $\vec\alpha\Rightarrow$ optimal $b$?  

根據primal feasible，$y_n(\textbf{w}^T\textbf{z}_n+b)\ge 1$，給出了 $b$ 的範圍(大部分(non-support vector)都大於1)。  
進一步，根據primal-inner optimal，$\alpha_n(1-y_n(\textbf{w}^T\textbf{z}_n+b))=0,\ \forall n$  
由於non-SV後面都是non-zero，因此 $\alpha_n=0$。因此若 $\alpha_n>0$，可以得出：  
$$  
\begin{align*}  
&1 - y_n(\mathbf{w}^T \mathbf{z}_n + b) = 0, \quad y_n(\mathbf{w}^T \mathbf{z}_n+b)=1 \\  
&y_n = \pm 1, \quad y_n = \frac{1}{y_n}\\  
&b = y_n - \mathbf{w}^T \mathbf{z}_n  
\end{align*}  
$$  

### High-level comments  

#### 比較 SVM, PLA  

| SVM                                                 | PLA                                                         |  
| :-------------------------------------------------- | :---------------------------------------------------------- |  
| $\textbf{w}_{SVM}=\sum_n \alpha_n(y_n\textbf{z}_n)$ | $\textbf{w}_{PLA}=\sum_n \beta_n(y_n\textbf{z}_n)$          |  
| $\alpha_n$從 dual solution。                        | $\beta_n=$ # of mistake corrections on $(\textbf{x}_n,y_n)$ |  

$\textbf{w}$ is linear combination of $y_n\textbf{z}_n$. This is also true for GD/SGD-based Logistic regression/Linear regression when $\textbf{w}_0=0$.  
$\textbf{w}$ is represented by data.  
SVM: represented by SVs only.  

#### 比較 primal 與 dual  

### Problems  

* 因為QP的kernel $Q$ 是一個 N-by-N 的矩陣，其中 $q_{n,m}=y_ny_m\textbf{z}_n^T\textbf{z}_m$ 大部分是Non-zero，因此當N大一點就會需要很多記憶體來存 $Q$。  
**解決**：practically用特殊的solver  
* 原本的目標：不要與轉換後的特徵數量 $\tilde{d}$ 相關，但其實如果真的去計算每個 $q_{n,m}=y_ny_m\textbf{z}_n^T\textbf{z}_m$，會是兩個 $\tilde{d}$ 長度的向量內積。  
**解決**：kernel SVM  

## Kernel Support Vector Machine  

目標：解決上述暴力計算 $q_{n,m}=\textbf{z}_n^T\textbf{z}_m\forall n,m\in [1,N]$ 時需要 $O(\tilde{d})$ 的問題。  


### Kernel function  

=Transform+Inner Product  
用有效的Kernel function快速計算 $\textbf{z}_n^T\textbf{z}_m=\Phi(\textbf{x}_n)^T\Phi(\textbf{x}_m)$  

Example for $\Phi_2$(poly transform)  
$\Phi_2(\textbf{x})=(1,x_1,\ldots,x_d,x_1^2,x_1x_2,\ldots,x_1x_d,x_2x_1,x_2^2,\ldots,x_d^2)$  

#### speed up Q for QP solver  

考慮計算  
$$  
\begin{align*}  
\Phi_2(\textbf{x})^T\Phi_2(\textbf{x}')&=1+\sum_{i=1}^d x_ix'_i+\sum_{i=1}^d\sum_{j=1}^d (x_ix_j)(x'_ix'_j)\\  
&=1+\sum_{i=1}^d x_ix'_i+\left(\sum_{i=1}^d x_ix'_i\right)\left(\sum_{j=1}^d x_jx'_j\right)\\  
&=1+\textbf{x}^T\textbf{x}'+(\textbf{x}^T\textbf{x}')^2  
\end{align*}  
$$  
> Note: $d$ 是原本資料的維度，而 $\tilde{d}=O(d^2)$ 是轉換後的維度，如果在 $O(d)$ 時間算完是可接受的。  

#### speed up b,w  



HTML week 11  
===  

## Soft-Margin Support Vector Machine  

## SVM for Soft Binary Classification  

## Blending and Bagging  

### An Aggregation Story  

> aggregation for binary classification  

假設有 $T$ 個朋友，每個人對一個股票的預測為 $g_1,\ldots,g_T$ 函數，對於股票 $x$，$\text{sign}(g_t(x))$代表漲跌。而根據這些朋友的結果做綜合的預測有哪些方法？  
* **select** 找表現最佳的朋友，只照抄他的預測，**validation**  
$G(x)=g_{t*}(x)$ with $t*=\text{argmin}_t E_{\text{val}}(g_t^-)$.  
* **mix** 所有朋友的預測，一人一票，**uniformly**  
$G(x)=\text{sign}(\sum_t 1\cdot g_t(x))$  
* **mix** 同上但是加上權重 $\alpha$，**non-uniformly**  
$G(x)=\text{sign}(\sum_t \alpha_t\cdot g_t(x))$ with $\alpha_t\ge 0$  
* **combine(stacking)** 預測什麼類股就主要參考那個類股的專家。權重depends on input，**conditionally**  
$G(x)=\text{sign}(\sum_t q_t(x)\cdot g_t(x))$ with $q_t(x)\ge 0$  

### 比較  
* Selection  
也就是第一種，很簡單也很常用， rely on strong hypothesis  
當然應該用 $E_{\text{val}}$ 而不是 $E_{\text{in}}$，但同樣的需要確保validation用的 $g_t^-$夠強  
* aggregation/blending  
參考其他弱一點的朋友(hypothesis)可能會更好  

### Why blending may be better  

* acts as feature transform: 把2D平面上只能用鉛直線的$\mathcal{H}_1$和只能用水平線的$\mathcal{H}_2$，blending後就可以用具有直角的線。  
* acts as regularization: 平均後，比如 linear regression 就能得到類似 SVM 的效果。  

### Blending for regression  

以uniform blending舉例  
$G=g_t$的平均，也就是 $G(x)=\frac{1}{T}\sum_t g_t(x)$  

#### Theoretical analysis for uniform blending  


$$  
\begin{align*}  
&\text{avg}_t(E_{\text{out}}(g_t))=\text{avg}_t((g_t(x)-f(x))^2)\\  
=&\text{avg}_t(g_t^2-2g_tf+f^2)\\  
=&\text{avg}_t(g_t^2)-2Gf+f^2\\  
=&\text{avg}_t(g_t^2)+(G-f)^2-G^2\\  
=&\text{avg}_t(g_t^2)-2G^2+G^2+(G-f)^2\\  
=&\text{avg}_t\left((g_t-G)^2\right)+(G-f)^2\\  
=&\text{avg}_t\left((g_t-G)^2\right)+E_{\text{out}}(G)\\  
\ge& E_{\text{out}}(G)  
\end{align*}  
$$  

Therefore, the uniform blending is better than the average of $g_t$.  

This can also be interpreted as:  
(expected performance of randomly choosing one hypothesis)  
= (expected deviation to consensus)  
\+ (performance of consensus).  

* performance of consensus: **bias**  
* expected deviation to consensus: **variance**  

Uniform blending reduces variance for more stable performance.  

HTML week 12  
===  

### Linear blending  

Known $g_t$, and each is given $\alpha_t$ ballots.  
$$  
G(x)=\text{sign}(\sum_t \alpha_t g_t(x))\text{ with }\alpha_t\ge 0  
$$  
Compute good $\alpha_t$: $\min_{\alpha_t\ge 0}E_{\text{in}}(\vec\alpha)$  
For linear regression(+transform), it looks alike.  
$$  
\min_{\alpha_t\ge 0}\frac{1}{N}\sum_{n=1}^N\left(y_n-\sum_t \alpha_t g_t(x_n)\right)^2  
$$  

有些 hypothesis 可能是反指標，所以 $\alpha_t$ 可以是負的，因此不一定需要 $\alpha_t\ge 0$ 的 constraints。  

### Any blending  

Blending 相當於把 $(x,y)$ 變換為 $(\Phi^-(x),y)$，其中 $\Phi^-(x)=(g_1^-(x),g_2^-(x),\dots)$。  
之後 Linear blending 相當於做 linear regression。  
事實上也可以用其他模型，也就是 **Any blending** ，相當於 Stacking(blending 權重與資料有關)。  
雖然很 powerful，但一樣會 overfitting。  

### Bagging  

如果能找出多樣化的 hypothesis，效果會更好。  
可能方法：  
* 每個 $g_t$ 用不同 hypothesis set  
* 用不同參數(learning rate等)  
* 隨機性的驗算法  
* 資料的隨機性(CV的不同資料切割，產生不同 $g_t^-$)  

而實際上可以用同一份資料利用資 料隨機性製造出不同的 $g_t$。  

#### Bootstrap aggregation  

$\tilde{D}_t$:  
* Sample $N$(or $N'$) data points **with replacement**(可能選到同筆資料很多次) from $\mathcal{D}$  
* Train $g_t$ by an algorithm $\mathcal{A}$ on $\tilde{D}_t$.  
* Do the above many times. Output the blending $G=\text{Uniform}(\{g_t\})$  

This simulates the real aggregation:  
* Request size-$N$ data from $P^N$(i.i.d.)  
* Train $g_t$ by an algorithm $\mathcal{A}$ on $\tilde{D}_t$.  
* Do the above many times. Output the blending $G=\text{Uniform}(\{g_t\})$  

因為我們沒有辦法真的每次得到不同的 $N$ 筆資料，所以重複取樣是一個近似的方法。  

又稱為 Bagging，把資料打包。  

#### bagging performance  

如果 hypothesis 對隨機資料很敏感(指產生多樣化的結果)，很有可能平均後的效果會很好。(像是沒教的 pocket algorithm)  

## Adaptive Boosting  

### 辨認蘋果問題  

叫一堆**小孩**講出可能的判斷方法：  
* 圓的  
* 紅色  
* 也有可能是綠色  
* 有可能長著梗  

過程中會得出一個**班級的共識**，**老師**再把錯誤的分類結果提出來讓**小孩**再想一想。  

對應到 ML  
* **小孩** = (simple, weak) hypothesis sets  
* **班級的共識** = blending 後的 hypothesis  
* **老師** = reweighting，讓 hypothesis 聚焦在錯誤的地方  

### Use Bootstrap Again  

Bootstrapping 相當於把N筆資料重新給予權重，有些可能是 0，有些可能是很多次。  
每個 $g_t$ 相當於在 minimize bootstrap-weighted error。  
$$  
E_{\text{in}}^u(h)=\frac{1}{N}\sum_{n=1}^N u_n\cdot err(h(x_n), y_n)  
$$  

### Weighted base algorithm  

可以重複某些資料，但也可以用演算法來達成，像是  
* soft SVM: 若是使用一個錯誤增加 $C$ 的 error，變成每次錯誤加 $Cu_n$ 就好。  
* 用 SGD 解 logistic regression: 調整 sample 到第 $n$ 筆的機率正比於 $u_n$。  

### More diverse results  

重複 T 次，第 t 次使用 $u^{(t)}$ 作為權重，我們希望每次結果會非常不同：  
* 用 $u^{(t)}$ 作為權重，得出 $g_t$  
* 我們希望 $g_t$ 在以 $u^{(t+1)}$ 作為權重時表現很差，因此 $g_{t+1}$ 會與 $g_t$ 有很大的差異。  
* 根據 $g_t$ 對不同的回答情況  

具體作法就是讓 $g_t$ 在以 $u^{(t+1)}$ 作為權重時的準確率為 0.5。  
我們想要：  
$$  
\frac{\sum_{n=1}^N u_n^{(t+1)}\cdot[\![g_t(x_n)\ne y_n]\!]}{\sum_{n=1}^N u_n^{(t+1)}}=0.5  
$$  
因此我們可以把 $u^{(t+1)}$設為：  
* 把 $g_t$ 在回答**正確**的 $n$ 的權重 $u^{(t+1)}_n$ 設為 $u^{(t)}_n$ 除以**正確**的比率  
* 把 $g_t$ 在回答**錯誤**的 $n$ 的權重 $u^{(t+1)}_n$ 設為 $u^{(t)}_n$ 除以**錯誤**的比率。  

或是交叉相乘：把正確的乘上**錯誤率**(次數)，錯誤的乘上**正確率**(次數)  

#### Scaling factor  

若 $g_t$ 在 $u^{(t)}$ 的錯誤率是 $\epsilon_t$。前一部分的方法相當於把正確的乘以 $\epsilon_t$，錯誤的乘以 $1-\epsilon_t$。  
因此可以取他們的中間值  
$$  
\text{Scaling Factor}=\mathcal{S}_t=\sqrt{\frac{1-\epsilon_t}{\epsilon_t}}  
$$  
正確時除以 $\mathcal{S}_t$，錯誤時乘以 $\mathcal{S}_t$。  

這會在之後用到。  

#### 如何決定 $u^{(1)}$  

Best for $E_{\text{in}}$，則用 $u^{(1)}_n=\frac{1}{N}$(相當於沒有 reweighting)。  

#### 如何決定 blending 方法 G  

不太可能用 uniform，因為 $g_2$ 是在正常的 $g_1$ 表現很差的資料訓練，這個資料會與原本的資料偏差很大，很有可能結果會很差，其他結果也是差不多。  
Linear 或 Non-linear 都行  

### AdaBoost  

使用特殊 blending 方法：  
$\alpha_t=\ln(\mathcal{S}_t)$，因為 Scaling Factor 與正確率正相關，所以相當於給越正確的 hypothesis 越多的權重。  

AdaBoost = 弱的 hypothesis(學生) + reweighting(老師) + blending(整個班)  

#### Theoretical guarantee  

If $\max(\epsilon_t)=\epsilon<\frac{1}{2}$, $E_{\text{in}}(G)=0$ after $T=O(\log N)$ iterations.  

### Decision Stump  

在某一維度上，用一個 threshold 來分類。非常弱，但很有效率。  
$N$ 筆 $d$ 維資料可以在 $O(d\cdot N\log N)$ 的時間完成。  

#### AdaBoost-Stump  

用 Decision Stump 作為 hypothesis，用 AdaBoost 來訓練。  
第一個實時辨認人臉的系統就是用這個方法，把圖片切成很多塊，並且用 Decision Stump 來判斷是否有人臉。  

### 補充  

* AdaBoost 很強大，因此要小心 overfitting。  
中小型的資料上可以用 (soft) SVM，可以達到類似的結果(regularization、margin)。  
* 在 $E_{\text{in}}=0$ 後繼續做還是可以降低 $E_{\text{out}}$，因為可以達到更小的 margin。  
* 比較適合二元分類，多元可以用 Gradient Boosting。  
* 比神經網路差。  

## Decision Tree  

Decision Tree 可以達到 conditional aggregation，也就是 stacking。  

| aggregation | blending | learning example |  
| :---------- | :------- | :--------------- |  
| uniform     | voting   | bagging          |  
| weighted    | linear   | boosting         |  
| conditional | stacking | Desicion Tree    |  

Decision tree 就是一堆 if-else 的組合，每個 if-else 就是一個 node。  
是個很接近人類邏輯的模型，也很容易解釋、很簡單(很多財經分析也許會用)、很有效率。但是沒有理論保證，不知道該怎麼選擇參數、沒有代表性的演算法。  

### 表示方法  

* Path: Summation for every path t, $G(x)=\sum_t q_t(x)\cdot g_t(x)$  
q: condition, g: leaf 上的 hypothesis（可以用常數）  
* Recursive: Summation for every child c $G(x)=\sum_c b_t(x)\cdot G_c(x)$  
b: child's condition, G: child's subtree's hypothesis  

### 建 Decision tree 的演算法  

* 停止條件  
到達應該做出葉節點的地方(termination criteria)則回傳  
* 如果要繼續  
  * 決定節點的條件 $b(x)$ (branching criteria)  
  * 分成不同的節點，遞迴建Decision Tree  
  * 回傳  

#### 需要選擇的事  
* 停止條件  
* 小孩數量  
* 節點分枝條件  
* 葉節點的 hypothesis  

### Classification and Regression Tree (CART)  

#### 節點分枝條件  
可以簡單的用 decision stump 來當作**節點分枝條件的 hypothesis set**，相對應的**小孩數量**就是 2(binary tree)。  

**節點分枝條件的決定**：盡量找出分群後的結果能讓**不純程度**(用 Impurity Function 決定)最小的 hypothesis。差不多相當於 error function。  
具體就是把不同群的 impurity function 以群的大小加權平均。  

##### Impurity Function  

* $E_{\text{in}}$ of optimal constant hypothesis:  
  * Regression with MSE: $\bar y=\text{avg}(y_1,\ldots,y_n)$, $\text{impurity}=\frac{1}{N}\sum_{n=1}^N(y_n-\bar y)^2$  
  * Classification with 0-1 loss: $y^*=\text{majority}(y_1,\ldots,y_n)$, $\text{impurity}=\frac{1}{N}\sum_{n=1}^N[\![y_n\ne y^*]\!]$  
* Special for classification  
  * Gini index: $N_k=\sum_{n=1}^N[\![y_n=k]\!]$, $\text{impurity}=1-\sum_{k=1}^K\left(\frac{N_k}{N}\right)^2$  
  考慮所有 $k$  
  * classification error: $\text{impurity}=1-\max_k\left(\frac{N_k}{N}\right)$  
  只考慮最常見的 $k=y^*$  

分類通常用 Gini index，回歸用第一種。  

#### 停止條件  

CART 是 **fully-grown** tree，因此會分到不能分為止，具體有這些條件：  
* Impurity=0，label 都一樣，沒辦法分  
* $x_n$ 都一樣，沒辦法分  

#### 葉節點的 hypothesis set  

因為結果會是不能繼續分的，可以直接用 optimal constant hypothesis。  

### Regularization by Pruning  

One regularizer: $\Omega(G)=\text{NumberOfLeaves}(G)$  
變成對於所有的 decision tree $G$，找到 $\text{argmin}_G E_{\text{in}}(G)+\lambda\Omega(G)$  
但當然無法找到所有的 decision tree，所以通常只會考慮：  
* $G^{(0)}$=fully-grown tree  
* $G^{(i)}$=$\text{argmin}_G E_{\text{in}(G)}$  
其中 $G$ 是從 $G^{(i-1)}$ 少掉一個葉節點。  

找到 $\lambda$ 的方法：validation  

### 用類別特徵分枝  

對應到 decision stump，會用 decision subset。  
$b(x)=[\![x_i\in S]\!]+1$，其中 $S\in[K]$  
一樣是個二元樹，所以就是一個包含於 $S$、一個不包含於 $S$。  

### Surrogate branching  

用其他類似的特徵來取代缺失的特徵。  
但實際上不一定能找到全部都沒有缺失的特徵，比如在 final project 大概就用不到。  

HTML week 13  
===  

## Random Forest  

用 bagging 的方法把 $T$ 個 Fully-grown Decision Tree 的輸出結合起來  

### OOB examples  

假設 bagging 每次抽 $N'=N$ 個，那每個 $t$ 沒抽到 $(x_n,y_n)$ 的機率是 $\left(1-1/N\right)^N$，當 $N$ 大了的話:  
$$  
  \left(1-\frac{1}{N}\right)^N=\frac{1}{\left(\frac{N}{N-1}\right)^N}=\frac{1}{\left(1+\frac{1}{N-1}\right)^N}\approx \frac{1}{e}  
$$  
每次大約會有 $N/e$ 個沒抽到，比想像中還多。  
用處: 可以對於每個 $g_t$ 剛好可以用它的 OOB examples 當作 validation。剛好就不用重新訓練。  

### 實測  

在複雜的資料上，也能得到很好的結果，這就是投票的力量。  

### T 要多少？  

越多越好，實際上大概需要幾千幾萬這個量級。  
壞處就是要算很多次 Decision Tree。  

## Gradient Boosted Decision Tree  

(Ada)Boost + Decision Tree  

<!-- todo -->  

HTML week 14  
===  

## Neural Network  

Intuition: 多個 perceptrons，加上 activation (模仿神經，用簡單的門檻，過某個值才是 1，否則是 0，相當於一個 perceptron 得到其他 perceptrons 的輸出作為輸入)，可以造出 AND OR NOT 等等的邏輯閘。多層的話就更強。  
為了簡化，用 MSE error。  



### Activation(Transformation)  

如果只是加起來，整個還是 Linear Model，所以沒差，提到 sigmoid、tanh，會提到為何 $\tanh$ 現在比較少用。  
$$  
\tanh(s)=\frac{\exp(s)-\exp(-s)}{\exp(s)+\exp(-s)}=2\theta(2s)-1  
$$  

### Hypothesis  

For a $d^{(0)}-d^{(1)}-\ldots-d^{(L)}$ Neural Network:  

$w_{ij}^{(l)}$  
* $1\le l\le L$: layers  
* $0\le i\le d^{(l-1)}$: inputs  
* $1\le j\le d^{(l)}$: outputs  

raw output  
$$  
s_j^{(l)}=\sum_{i=0}^{d^{(l-1)}} w_{ij}^{(l)}x_i^{(l-1)}  
$$  
transformed output  
$$  
x_j^{(l)}=  
\begin{cases}  
  A(s_j^{(l)}) ,&\text{if $l<L$}\\  
  s_j^{(l)} ,&\text{if $l=L$}  
\end{cases}  
$$  

> universal approximator:  
> Neural Network 能夠模仿任何函數，實際上就算只有一層，只要 neuron 夠多也可以達到。像是 Gaussian Kernel 很強的概念一樣。  

> adaboost 難以與 perceptron 並用。  

可以用(stochastic)gradient descent來minimize loss(error)  
簡單暴力的把error對w取偏微分，會得到de/dw=de/ds*ds/dw，但除了輸出層的s直接與e關連，其他需要用 backward propagation 算。  

#### automatic differentiation  

直接真的用很少的偏移看看結果差多少作為微分結果。  

### optimize gives local minimum  

如果只用 gradient descent，只會得到 local minimum，因此 init weights 很重要，像是太大的話梯度很小，會「飽和」，可以試試看小又隨機的 weight。  
但後來發現其實不太會跑到 bad local minimum，只要用經驗法則選好的 weights 就好了。或是**pre-training**  

### initialization  

* 全 0，tanh relu都無法運作  
* 一樣，所有 neuron 都長一樣  
* 太大，梯度消失(tanh 出來的值差不多)  

因此需要 small and random  

### Regularization  

Early Stopping: 因為 gradient descent 類型的 model 在步驟多了之後會探索更多區域，相當於 $d_{vc}$ 漸漸增大，因此可以用 validation error 早點停下來。但有可能 validation error, $E_{out}$ 會在之後再次下降。  
這是早期流行的方法，現在會用 double descent，  

## Deep learning  

### Pre-training  

* shallow networks: RBM，可以把其他層固定，每次只訓練幾層。  
* other tasks: 用 self-supervised learning 做 foundation model  

## Activation and Initialization  
<!-- todo -->  

## Optimization in Deep Learning  
<!-- todo -->  