---
title: TAMC 筆記
tags: [2024_Fall]
---
<!-- HackMD ID:nl89K4CtSjObpBfyi14h_A -->  

TAMC 筆記  
===  
# week 3  

## Hardness Amplification(Concrete ver.)  

By reduction, suppose $f_k$ is not $(t',\epsilon')-OW$. That is $\exists Adv^{f_k}$ break $(t',\epsilon')-OW$ for $f_k$. Construct R to break $(t,\epsilon)-OW$ for $f$.  

### Reduction  

$\forall i\in[k]$, let $y_i=y, \vec{x_{-i}}\leftarrow \{0,1\}^{n(k-1)}$, let $\vec{y_{-i}}=f(\vec{x_{-i}})$. Compute $\vec{x'}=Adv^{f_k}(\vec{y})$ for $\frac{2kn}{\gamma}$ times for each $i$. If $Adv^{f_k}$ wins, or $f_k(\vec{x'})=\vec{y}$, then $R(y)=x$ and $R$ wins.  

### Obs  

for $i\in[k]$, $x\leftarrow \{0,1\}^n, y_{i}=f(x)$.  
If  
$$  
\text{For }x,\Pr[Adv^{f_k}(y_i,y_{-i})\text{ wins}] \ge \frac{\gamma}{2k}  
$$  
$$  
\Rightarrow \Pr[Adv^{f_k}\text{ fails in all }\frac{2kn}{\gamma}\text{ tries}] \le e^{-n}  
$$  

### Define a good set  

Define good set $G_i\subseteq\{0,1\}^n$ as:  
$$  
G_i\{x\in\{0,1\}^n|\Pr[Adv^{f_k}(y_i,y_{-i})\text{ wins}]\ge \frac{\gamma}{2k}\}  
$$  
$$  
x\in G_i \Rightarrow\text{R can win w.h.p. }\ge 1-e^{-n}  
$$  
(w.h.p.=with high probability)  
WTS $\exists i\in[k]$ s.t. $G_i$ is large enough.  

### Claim  

$\exists i\in[k]$ s.t. for x, $\Pr[x\in G_i]\ge (1+\delta)\cdot \epsilon$. Then  
$$  
\begin{align*}\Pr[R\text{ wins}]&\ge\Pr[R\text{ wins}\land x\in G_i]\\  
&=\Pr[R\text{ wins} | x\in G_i]\cdot \Pr[x\in G_i]\\  
&>(1-e^{-n})\cdot(1+\delta)\epsilon\\  
&>\epsilon  
\end{align*}  
$$  

#### Proof of Claim:  
Suppose not. $\forall i\in[k]$, $\Pr[x\in G_i]<(1+\delta)\cdot \epsilon$  
we show $\Pr[Adv^{f_k}\text{ wins}]<\epsilon'=[(1+\delta)\epsilon]^k+\gamma$  
$$  
\begin{align*}  
&\Pr[Adv^{f_k}\text{ wins}]\\  
=&\Pr[Adv^{f_k}\text{ wins} \land (\exists i, x_i\notin G_i)]+\Pr[Adv^{f_k}\text{ wins} \land (\forall i, x_i\in G_i)]\\  
<&[(1+\delta)\epsilon]^k+\frac{\gamma}{2}  
\end{align*}  
$$  


### Computation time of $R$:  

* Call $Adv^{f_k}$ $\frac{2k^2n}{\gamma}$ times $\Rightarrow O(\frac{2k^2n}{\gamma}t')$ time.  
* Call $f(x)$ to validate the answer: $O(\frac{2k^3n}{\gamma})$ times  
$\frac{2k^2n}{\gamma}t'+\frac{2k^3n}{\gamma}\times t_f<t$  
$t'=O(\frac{\gamma}{k^3n}\cdot t)$ provided that $t'\ge kt_f$, where $t_f$ is the computation time of $f$.  

## Computational Indistinguishability and Pseudorandomness  

Some distributions:  
* uniform dist. $\mathcal{U}_n$: $\Pr[\mathcal{U}_n=x]=2^{-n}\forall x$  
* random image. for some $f:\{0,1\}^n\to \{0,1\}^m$, $f(\mathcal{U}_n)$  
* uniform over $S$: $\mathcal{U}_S$  
$$  
\Pr[\mathcal{U}_S=x]=  
  \begin{cases}  
    1/|S| & x\in S \\  
    0 & \text{otherwise}  
  \end{cases}  
$$  

### Definition of comp. indist. (Concrete ver.)  

$X,Y$ dist. over $\{0,1\}^n$ is $(t,\epsilon)$-comp. indist. if $\forall$ PPT distinguisher $D$ running in $t$,  
$$  
|\Pr[x\leftarrow X:D(x)=1]-\Pr[y\leftarrow Y:D(y)=1]|\le\epsilon  
$$  
denoted as $X\approx_{t,\epsilon} Y$  

### Definition of Pseudorandom (Concrete ver.)  

$X$ dist. over $\{0,1\}^n$ is $(t,\epsilon)$-pseudorandom if $X\approx_{t,\epsilon} \mathcal{U}_n$  

### Fun fact  

$\exists S\subseteq\{0,1\}^n$, $|S|=2^{0.1n}$. s.t. $\mathcal{U}_S$ is $(n^{\log n}, n^{-\log n})$-pseudorandom.  

### Definition of comp. indist.  

${X_n},{Y_n}$ is comp. indist. if $\forall$ PPT distinguisher $D$, $\exists \text{negl} \nu$ s.t. $\forall$ suff. large n, $|\Pr[x\leftarrow X:D(x)=1]-\Pr[y\leftarrow Y:D(y)=1]|\le \nu(n)$  
denoted as $\{X_n\}\approx_c \{Y_n\}$  

### Definition of Pseudorandom Generator(PRG)  

$G_n:\{0,1\}^n\to\{0,1\}^{m(n)}$ is PRG if  
* Efficiency: $G$ can be computed efficiently  
* Expansion: $m(n)>n$  
* Pseudorandom: $\{G_n(\mathcal{U}_n)\}_n \approx_c \{\mathcal{U}_{m(n)}\}_n$  

# week 4  
![PXL_20241009_022449352~3](https://hackmd.io/_uploads/HyMLgxEgJx.jpg)  
![PXL_20241009_022457422~3](https://hackmd.io/_uploads/rJ-IxxVg1l.jpg)  

# week 6  

## oracle  

An oracle $\mathcal{O}$ is a (potentially randomized) “black-box” function $\{\mathcal{O}_n : \{0,1\}^n \to \{0,1\}^{m(n)}\}_{n\in\mathbb{N}}$ that can be queried by an algorithm. Specifically, on input query x, the oracle $\mathcal{O}$ returns $y = \mathcal{O}(x)$.  

## Oracle algorithm  

An oracle algorithm $\mathcal{A^O}$ is an algorithm that is given oracle access to an oracle $\mathcal{O}$. Namely, $\mathcal{A}$ can make an arbitrary number of oracle queries $x$ to $\mathcal{O}$ and receive answers $y = \mathcal{O}(x)$ during its computation.  

## keyed function  

$f:\{0,1\}^{l(n)}\times\{0,1\}^n\to\{0,1\}^n$  
$f_k(x)=f(k,x)$  

## PRF(Pseudorandom Function)  

A keyed function $f:\{0,1\}^{l(n)}\times\{0,1\}^n\to\{0,1\}^n$ is PRF if ~~for a fixed $k$, f(k,x) is pseudorandom~~ (not possible because there are exponential $k$'s, even only checking all $f(k,x)$ in linear time will cost exponential time).  
The correct definition:  
$|\Pr[k\gets \{0,1\}^{l(n)}:D^{f_k}(1^n)=1]-\Pr[H\gets RF_n:D^H(1^n)=1]|\le \mu(n)$  
$RF_n$ is the uniform distribution of uniformly random functions that maps n-bit strings to n-bit strings.  
In the form of a game:  
* Ch samples $b\gets \{0,1\}$  
    * if $b=0,\ f\gets RF_n$.  
    * if $b=1,\ k\gets U_{l(n)},\ f=f_k$  
* Adv can query polynomial times of f(x).  
* If Adv returns $b'=b$, then Adv wins.  

## thm: PRG implies PRF  

## GGM's construction  

GGM(Goldreich-Goldwasser-Micali) is a way to construct PRF  
Let PRG $G:\{0,1\}^n\to\{0,1\}^{2n}$, $G(x)=G_0(x)|G_1(x)$.  
Input: $x\in\{0,1\}^n$, sample $k\gets U_n$, and output $f_k(x)=G_{x_{n-1}}\circ\cdots\circ G_{x_0}(k)$  

### Hybrid argument  

GOAL: show that $G(U_n^{(0)})|\cdots |G(U_n^{(t)})$ and $U_n^{(0)}|\cdots |U_n^{(t)}$ are indistinguishable.  
Define $Hyb_i:$  

* if $1\le i<t$, $k_1,\ldots,k_i\gets U_{2n}$, and $k_{i+1},\ldots,k_t\gets U_n$. Output $(k_1,\ldots,k_i,G(k_{i+1}),\ldots,G(k_t))$  
* Define $Hyb_0=G(U_n^{(0)})|\cdots |G(U_n^{(t)}$  
* Define $Hyb_t=U_n^{(0)}|\cdots |U_n^{(t)}$  

Let $P_i=\Pr[D(Hyb_i)=1]$  
Suppose for contradiction that $|P_0-P-t|>\frac{1}{n^c}$, where $\frac{1}{n^c}$ is non-negligible.  
By triangle inequality,  
$$  
\begin{align*}  
|P_0-P_t|&=|P_0-P_1+P_1-P_2+\ldots+P_{t-1}-P_t|\\  
&\le |P_0-P_1|+\ldots+|P_{t-1}-P_t|  
\end{align*}  
$$  
By averaging argument, there exists an $0\le i\le t-1$ such that $|P_i-P_{i+1}|>\frac{1}{n^ct}$. This breaks the assumption that $G$ is a PRG.  
**Note:** t mustn't be exponential of n, otherwise $\frac{1}{n^ct}$ is negligible.  

### GGM analysis  

Hint: construct a polynomial number of Hybrids.  
Observation: GGM is a binary tree with height $n$, so there are $2^n$ leaf nodes of n-bits string.  
* First attempt: $Hyb_i$ means the i's leaf nodes are replaced with $U_n$. This won't work because there is an exponential number of Hybrids.  

#### Correct attempt: $Hyb_i$ means:  

* $g:\{0,1\}^i\to\{0,1\}^n, \forall y\in\{0,1\}^i, g(y)\gets U_n$  
* if $i=0$, normal GGM. $k\gets U_n$, $f(x)=G_{x_{n-1}}\circ\cdots\circ G_{x_0}(k).$  
* if $0<i<n$, $f(x)=G_{x_{n-1}}\circ\cdots\circ G_{x_i}(g(x_{i-1}\ldots x_0))$  
* if $i=n$, f(x)=g(x)  

Equivalent to replacing the i-th layer of the tree to be all independent $U_n$. Upper layers(0~i-1) don't matter.  

#### Construct a reduction  

* Ch samples $b\gets \{0,1\}$  
    * if $b=0$, $\forall i\in[t], k_i\gets U_n, s_i=G(k_i)$  
    * if $b=1$, $\forall i\in[t], s_i\gets U_n$  
* R:  
    * $s_i^0=s_i[1:n/2],s_i^1=s_i[n/2+1:n]$  
    * For each  

# week 7  

## PKE(Public key encryption)  

$PKE=(Key Gen, Enc, Dec)$  
| Alice                   |      | Bob              |  
| ----------------------- | ---- | ---------------- |  
| $(pk,sk)\gets Gen(1^n)$ | pk-> | $ct=Enc_{pk}(m)$ |  
| m'=Dec{sk}(ct)          | <-ck |                  |  

ct:cipher text, $ct\in\mathcal{C}_n$  
The channel(pk,ct) may be public(everyone can access it), but assumed to be authenticated(no one can modify content).  
$Enc$ may have randomness: $Enc_{pk}(m;r)$  
$Dec$ is deterministic, outputting m or $\perp$(invalid)  

### Property: Correctness  

$\exists\mu=negl(n), s.t. \forall n\in\mathbb{N},m\in \mathcal{M}_n$  
$$  
\Pr[(pk,sk)\gets Gen(1^n),Dec_{sk}(Enc_{pk}(m))=m]\ge 1-\mu(n)  
$$  

## Different security definition  

### OW-CPA  

CPA: Chosen-Plaintext Attack  

| Ch                      |         | Adv                |  
| ----------------------- | ------- | ------------------ |  
| $(pk,sk)\gets Gen(1^n)$ |         |                    |  
| $m\gets \mathcal{M} _n$ |         |                    |  
| $ct=Enc_{pk}(m)$        | pk,ct-> | $m'=   Adv(pk,ct)$ |  
| Adv wins if $m'=m$      | <-m'    |                    |  

Secure if $\exists \text{ negl } \mu, s.t. \forall n\in\mathbb{N}, \Pr[Adv\text{ wins}]\le \mu(n)+\frac{1}{|\mathcal{M}_n|}$  

#### Problem  

保證的是不能還原全部訊息，但如果被還原部分訊息還是很危險。  

### IND-CPA  

| Ch                      |                             | Adv |  
| ----------------------- | --------------------------- | --- |  
| $(pk,sk)\gets Gen(1^n)$ | pk->                        |     |  
| $b\gets\{0,1\}$         | <-$m_0,m_1\in\mathcal{M}_n$ |     |  
| $ct=Enc_{pk}(m_b)$      | ct->                        |     |  
| $Adv$ wins if $b'=b$    | <-b'                        |     |  

Secure if $\exists \text{ negl } \mu, s.t. \forall PPT Adv, n\in\mathbb{N}, \Pr[Adv\text{ wins}]\le \frac{1}{2}+\mu(n)$  

#### Problem  

Some other people (Eve) may ask Alice what $m$ corresponds to a cipher text $ct$. And find some patterns in its reaction.  

### IND-CCA  

CCA: Chosen-Ciphertext Attack  

| Ch                      |                             | Adv |  
| ----------------------- | --------------------------- | --- |  
| $(pk,sk)\gets Gen(1^n)$ | pk->                        |     |  
|                         | <-$ct_i$(Multiple times)    |     |  
|                         | $m_i=Dec_{sk}(ct_i)$->      |     |  
| $b\gets\{0,1\}$         | <-$m_0,m_1\in\mathcal{M}_n$ |     |  
| $ct=Enc_{pk}(m_b)$      | ct->                        |     |  
|                         | <-$ct_i$(Multiple times)    |     |  
|                         | $m_i=Dec_{sk}(ct_i)$->      |     |  
| $Adv$ wins if $b'=b$    | <-b'                        |     |  

先試很多次再收問題，然後可以再試很多次。  
Secure定義和IND-CPA一樣  
限制$ct_i\neq ct$  
等價定義：Adv given access to an oracle $\mathcal{O}(ct)=Dec_{sk}(ct)$  

## Assumptions  

* Group-based: 量子電腦可破解  
* Lattice-based: 後量子都可以用  

### Group-based Assumption  

cyclic group:$(G,q,g)$, which includes $\{id,g,g^2,g^3,\ldots,g^{q-1}\}  
Ex: $Z_p^*=\{1,g,g^2,\ldots,g^p-2\}$, where $p$ is a prime.  
不care group的細節，但大概會是從elliptic curve group來  
Suppose some efficient operations: $g\cdot h, g\mapsto g^t, \mapsto g^{-1}$  
Hard operation problems:  
* ex: discrete log  
    * input:$h=g^x$  
    * output:$x$  

#### DL assumption for $(G,q,g)$  

| Ch                 |           | Adv |  
| ------------------ | --------- | --- |  
| $x\gets Z_q$       | $h=g^x$-> |     |  
| Adv wins if $x'=x$ | <-x'      |     |  

$\forall PPT\ Adv,\exists \text{negl }\mu, s.t. \forall n, \Pr[Adv\text{ wins}]\le \mu(n)$  

某些prime簡單，某些prime難  

最弱的assumption，要造PKE需要更強的assumption  

#### DDH assumption for $(G,q,g)$  

DDH: decisional Diffie–Hellman problem  

* sample $x,y,z\gets Z_q$  
* $(g,g^x,g^y,g^{xy})\approx_c(g,g^x,g^y,g^z)$  

Can distinguish $g^{xy}$ and $g^z$ given $g,g^x,g^y$.  
Game就不寫了  
滿好用的，可以造PKE  

**Search version**:CDH(computational Diffie–  
Hellman)  
Given $g,g^x,g^y$, compute $g^{xy}$.  

## PKE from DDH for $(G,q,g)$  

El Gamal PKE=$(Gen,Enc,Dec)$  
* $Gen(1^n)\to (pk,sk)$  
    * sample $s\gets Z_q$  
    * output $sk=s,pk=g^s$ (sk is hidden from pk)  
* $Enc_{pk}(m)\to ct$, $\mathcal{M}_n=G$  
    * sample $r\gets Z_q$  
    * $ct=(g^r,pk^r\cdot m)\ (=(g^r,g^{sr}\cdot m))$  
* $Dec_{sk}(ct)$:  
    * input $ct=(u,v)$  
    * output $v\cdot u^{-sk}$  

**Correctness**:  
$ct=(g^r,g^{sr}\cdot m)$  
$v\cdot u^{-sk}=(g^{sr}\cdot m)(g^r)^{-s}=m$  

## Thm: Assume DDH, El Gamel PKE is IND-CPA-secure  

Suppose not, $\exists PPT\ Adv$ breaks IND-CPA-secure. That is, $\exists \epsilon(n)=\frac{1}{poly(n)}$, such that  

| Ch                           |                            | Adv |  
| ---------------------------- | -------------------------- | --- |  
| $(s,g^s)\gets Gen(1^n)$      | $pk=g^s$->                 |     |  
| $m_1\gets G(=\mathcal{M}_n)$ | <-$m_0$                    |     |  
| $b\gets \{0,1\}$             |                            |     |  
| $ct=Enc_{pk}(m_b)$           | $ct=(g^r,g^{sr}\cdot m)$-> |     |  
| Adv wins if $b'=b$           | <-$b'$                     |     |  

$\Pr[Adv\text{ wins}]\ge\frac{1}{2}+\epsilon(n)$  
Claim: 給Adv選$m_0,m_1$和只給他選$m_0$，$m_1$隨機選是等價的  

### Construct a reduction R to break DDH  

| Ch                   |                     | R   |                           | Adv |  
| -------------------- | ------------------- | --- | ------------------------- | --- |  
| $x,y,z\gets Z_q$     |                     |     |                           |     |  
| $b\gets \{0,1\}$     |                     |     |                           |     |  
| $w_0=g^{xy},w_1=g^z$ | $(g,g^x,g^y,w_b)$-> |     | $pk=g^x$->                |     |  
|                      |                     |     | <-$m_0$                   |     |  
|                      |                     |     | $ct=(g^y,w_b\cdot m_0)$-> |     |  
|                      | <-$b'$              |     | <-$b'$                    |     |  

# week 9  

Lattice-based Assumption  

## Learning with error(LWE) problem  

Let $n\in\mathbb{N}$ be the security parameter, $q(n)$ be a modulus(poly or $n^{\omega(1)}$), $m(n)>\Omega(n\log n)$ and $\chi$ be an error probability distrubution over $\mathbb{Z}_q$ (usually discrete Gaussian distribution).  

A sample from LWE distribution $LWE_{n,m,q,\chi}\in \mathbb{Z}_q^{m\times n}\times \mathbb{Z}_q^m$ is generated by:  
* $A\gets \mathbb{Z}_q^{m\times n}$  
* $s\gets \chi^n\subset\mathbb{Z}_q^n$(直接從$\mathbb{Z}_q^n$也可以)  
* $e\gets \chi^m\subset\mathbb{Z}_q^m$  

Output $(A,b=As+e)$  

### $\chi$ over discrete Gaussian distribution  

**胖度** $\alpha q$: discrete Gaussian distribution 中間高起來的寬度（幾標準差）  
$q\gg\alpha q>2\sqrt{n}$  

### LWE assumption  

* $A'\gets\mathbb{Z}_q^{m\times n}$  
* $u\gets\mathbb{Z}_q^m$  

$(A,b)\approx_c (A',u)$  

#### comment  

If $b=As$, we can easily distinguish them by trying to solve s. $s$ is $n$-dimensional and we map to $b$, so $b$ is also $n$-dimensional. $u$ is $m$-dimensional, so it's unlikely to be solved.  
直覺：$\chi$越胖越難解  

## SKE from LWE  

會比較簡單一點  

$SKE=(Gen, Enc, Dec)$  
* $Gen(1^n)$  
    * Output $sk=s\gets \chi_q^n$  
* $Enc_{sk}(m)$, $m\in\{0,1\}$  
    * Sample $a\gets \mathbb{Z}_q^n$, $e\gets \chi$  
    * Let $b=a\cdot s+e$  
    * Output $ct=(a,b+m\cdot\lfloor\frac{q}{2}\rfloor)$  
* $Dec_{sk}(ct)$, $ct=(u,v)$  
    * Let $z=v-u\cdot sk$  
    * Output $\begin{cases}  
0,\text{ if }z\in [-\frac{q}{4},\frac{q}{4}]\\  
1,\text{ otherwise}  
\end{cases}$  

### Correctness  

$$  
\begin{align*}  
z&=v-u\cdot sk\\  
&=(b+m\cdot\lfloor\frac{q}{2}\rfloor)-a\cdot s\\  
&=m\cdot\lfloor\frac{q}{2}\rfloor+e  
\end{align*}  
$$  
因此不會與$m$差太多  

## Regev's PKE  

$PKE=(Gen, Enc, Dec)$  
* $Gen(1^n)$, $q=q(n), m=m(n), \chi=\Psi_{\alpha(n)}$  
    * Sample $A\gets \mathbb{Z}_q^{m\times n}$  
    * Sample $s\gets\chi^n, e\gets \chi^m$  
    * Let $pk=(A,b=As+e), sk=s$  
* $Enc_{pk}(m)$, $m\in\{0,1\}$  
    * Sample $r\gets \{0,1\}^m$, $e\gets \chi$  
    * Output $ct=(r^TA,(r^Tb)+m\cdot\lfloor\frac{q}{2}\rfloor)$  
* $Dec_{sk}(ct)$, $ct=(u,v)$  
    * Let $z=v-u\cdot sk$  
    * Output $\begin{cases}  
0,\text{ if }z\in [-\frac{q}{4},\frac{q}{4}]\\  
1,\text{ otherwise}  
\end{cases}$  

### Correctness  

$ct=(r^TA,(r^Tb)+m\cdot\lfloor\frac{q}{2}\rfloor)$  
$$  
\begin{align*}  
z&=v-u\cdot sk\\  
&=(r^Tb+m\cdot\lfloor\frac{q}{2}\rfloor)-r^TAs\\  
&=(r^TAs+r^Te+m\cdot\lfloor\frac{q}{2}\rfloor)-r^TAs\\  
&=r^Te+m\cdot\lfloor\frac{q}{2}\rfloor\approx m\cdot\lfloor\frac{q}{2}\rfloor  
\end{align*}  
$$  

## Thm: Regev's PKE is IND-CPA secure  

Suppose not, $\exists PPT\ Adv$ breaks IND-CPA-secure. That is, $\exists \epsilon(n)=\frac{1}{poly(n)}$, such that  

| Ch                      |                 | Adv |  
| ----------------------- | --------------- | --- |  
| $(pk,sk)\gets Gen(1^n)$ | $pk=(A,b)$->    |     |  
| $B\gets \{0,1\}$        | <-$m_0=0,m_1=1$ |     |  
| $ct=Enc_{pk}(m_B)$      | $ct$->          |     |  
| Adv wins iff $B'=B$     | <-$B'$          |     |  

$\Pr[Adv\text{ wins}]\ge\frac{1}{2}+\epsilon(n)$  

### Adversary's view  

$Adv$ is given $(A,b,m_0,m_1,r^TA,(r^Tb)+m_B\cdot\lfloor\frac{q}{2}\rfloor)$  

### Hybrid argument Step 1  

Think of LWE assumption, change the public key given to Adv from $(A,b)$ to $(A,u)$, where $u\gets\mathbb{Z}_q^m$.  
Claim:  
$(A,b,m_0,m_1,r^TA,(r^Tb)+m_B\cdot\lfloor\frac{q}{2}\rfloor)$ $\approx_c(A,u,m_0,m_1,r^TA,(r^Tu)+m_B\cdot\lfloor\frac{q}{2}\rfloor)$  
So given $(A,u)$, $Adv$ can also win with a non-negligible advantage.  

### Hybrid argument Step 2  

Claim: $r^TA$ and $r^Tu$ are pseudorandom.  
$(A,u,m_0,m_1,r^TA,(r^Tu)+m_B\cdot\lfloor\frac{q}{2}\rfloor)$ $\approx_s(A,u,m_0,m_1,u_1,u_2)$  
where $u_1\gets\mathbb{Z}_q^n, u_2\gets\mathbb{Z}_q$.  
Given the cipher text is random, $Adv$ can also solve the message. **Impossible!**  

### Leftover hash lemma  

Let $A\gets \mathbb{Z}_q^{m\times n}$, $\epsilon>0$, $r\gets \{0,1\}^m$, $u\gets \mathbb{Z}_q^n$  
where $m\ge n\log q+2\log\frac{1}{\epsilon}+O(1)$  
Then $\Delta((A,r^TA,),(A,u))\le \epsilon$  

For the Hybrid argument Step 2  
$\begin{bmatrix} r^T \end{bmatrix}  
\begin{bmatrix} A & u \end{bmatrix} =  
\begin{bmatrix} u_1^T & u_2 \end{bmatrix}$  
Increase $n$ by 1, the result still holds.  

### Problem  

The public key includes a $A:m\times n$ matrix, which may be too expensive.  
It can be solved by Ring LWE instead of Module LWE.  

# week 10 FO transformation  

El Gamel's and Regev's PKE are not IND-CCA-secure.  
Assuming RO(Random oracle), given an OW-CPA/IND-CPA-secure PKE, we can transform it into an IND-CCA-secure PKE. Practically, we will simulate the RO with a hash function. For post-quantum security, we need quantum RO.  

$IND-CPA \overset{T\ Trans}\to OW-CCA\overset{U\ Trans}\to IND-CCA(KEM)$  
KEM:可以想像成先用PKE產生一個雙方都知道的random key，然後用SKE。  

## RO Model  

RO: a deterministic random function, for each input the output is uniformly random. Deterministic means the same input will always lead to the same output.  
所有人都共用一個RO  

## Lazy Sampling  

As in GGM. Initialize an empty table. For each query, output the entry if there is, otherwise sample one and return it.  

## RO Heuristic  

## OW-CCA  

和OW-CPA很像，但加上adversary可以query $Dec_{sk}(ct')$，但$ct'\neq ct$  
更強的版本: 可以call $G(m)$(Enc的隨機性來源)  

## T Transform  

For an IND-CPA PKE $(Gen, Enc, Dec)$, with a random oracle, we can construct an OW-CCA PKE $(Gen', Enc', Dec')$.  
* $Gen'=Gen$  
* $Enc'_{pk}(m)=Enc_{pk}(m;G(m))$  
* Let $m'=Dec_{sk}(ct)$  
    * If $m'\neq \perp$ and $Enc_{pk}(m';G(m'))=ct$, return $ct$. (the )  
    * Otherwise $\perp$  

Note that the T transform outputs a deterministic PKE.  

### reduction  

R用Adv(breaks OW-CCA) break IND-CPA:  
* **How to decide $m_0,m_1$?**  
Because R has no information, $m_0,m_1\gets M$  
* **R has no access to RO but needs to simulate RO**  
By lazy sampling  
* **How does R decide answer?**  
If Adv wins, $m'=m_0/m_1$, so output $0/1$ (II)  
else output a random bit. (III)  
 * **What if Adv queries $m_0$ or $m_1$?**  
 Since R doesn't know $b$ or the $r$ that Ch uses, it cannot just randomly sample the answer, otherwise, the distribution is wrong(G(m_b) for Ch is not the same as for Adv).  
 If get $m_0/m_1$, output $0/1$. See it as the Adv finds the answer and ensures it's true. (I)  

For the  

## U Transform  

# week 11 Digital Signature  

## Signature  

避免攻擊者傳送偽造或變造的訊息給接收者  

## Definition  

digital signature scheme=$(Gen, Sign, Vrfy)$ Vrfy=Verify  

| Signer                   |               | Verifier                |  
| :----------------------- | :------------ | :---------------------- |  
| $(pk,sk)\gets Gen(1^n)$  | pk->          |                         |  
| $\sigma\gets Sign(sk,m)$ | $\sigma, m$-> | $0/1=Vrfy(pk,m,\sigma)$ |  

Completeness:  
$$  
\forall m,\ \Pr[Vrfy(pk,m,Sign(sk,m))=1]=1-negl(n)  
$$  

## EUF-CMA Secure  

Adv 給定 $pk$，可以 query Ch 很多次 $m_i$，並得到對應的 $\sigma_i$，最後若能給出一對 $m,\sigma$ 使得 $Vrfy(pk,\sigma,m)=1$ 且 $m$ 沒有出現過，則 Adv 成功偽造(Forge)了一個簽章。這個機率要是negligible($\sigma$ 的 space 很大)  

## DL assumption to Schnorr Signature Scheme  

[DL(discrete log) assumption](#DL-assumption-for-Gqg)  

Schnorr signature scheme(in ROM) is group-based:  
| Signer                        |               | Verifier                                       |  
| :---------------------------- | :------------ | :--------------------------------------------- |  
| $s\gets \mathbb{Z}_q, pk=g^s$ | $(G,g,pk)$->  |                                                |  
| $k\gets \mathbb{Z}_q$         |               |                                                |  
| $\sigma=(g^k,H(g^k,m),k-sc)$  | $\sigma, m$-> | check if $c=H(g^k,m)$ & $g^z=\frac{g^k}{pk^c}$ |  

直覺會覺得要破Schnorr無論如何都需要破discrete log  
證明需要許多步驟：  

### Sigma Protocol  

#### NP relation  

An NP relation is a binary relation $R\subset X\times Y$. Elements of X are called statements. If $(x,y)\in R$, y is called a witness for x.  

Example:  
1. The three coloring problem. X=graph, Y=coloring，則 R 就是 (graph,對應的合法塗色方式) 的集合。  
2. Discrete log problem. $R=\{(x,y)|x=(g,g^s),y=s\}$ is a NP-relation.  

Prover想證明對於某個問題的某個x，他有答案y，但不想把答案透漏給Verifier，因此：  
| Prover |                   | Verifier                  |  
| :----- | :---------------- | :------------------------ |  
|        | Commit(Com) ->    |                           |  
|        | <- Challenge(Ch)  |                           |  
|        | Response(Resp) -> | $0/1=Vrfy(x,Com,Ch,Resp)$ |  

當y真的是答案(is a witness for x) $(x,y)\in R$，V永遠輸出1：  
$$  
\Pr[\langle P(x,y),V(x)\rangle=1]\ge 1-negl(n)  
$$  
角括號代表兩者互動過程中V的輸出  

### Special Soundness  

一個(P,V)有special soundness，如果有一個PPT algorithm Ext(a witness extractor) such that 若input為 x，與對應的任兩個相異($Ch\neq Ch'$)互動過程 $(Com,Ch,Resp),(Com,Ch',Resp')$，Ext可以輸出正確的y，即$(x,y)\in R$。  
**Note**: 但是要有同樣的 $Com$！  

### Honest Verifier Zero Knowledge(HVZK)  

一個(P,V)是HVZK，如果有一個PPT algorithm Sim，input x，輸出$(Com,Ch,Resp)$的分布與$(P,V)$互動過程一樣。  
Ex: DL problem:  
$(r,c,z)$當中，原本 $r=g^k$ 與 $c$ 是 uniformly random，而 $z=k-sc$ 是兩者 deterministically 決定。但其實 $(c,z)$ 的 marginal probability 也是 uniform 的，所以我們可以先 sample $(c,z)$ 再算出 $r$。  
已知 $g, g^s$，所以 $r=g^k=g^{z+sc}=g^z\cdot (g^s)^c$。  
且輸出的 distribution 與原本的相同(都是 uniform)  

HVZK 的意思是在 verifier 是誠實(c 確實是 random)的情況下，會是 zero knowledge。  

**Note**: 有 Simulator 也不能 forge signature，因為 Verifier 問的 Ch 幾乎不會是 Simulator 生出來的。  

### DL Assumption to DL Relation is Avg-Hard  

# week 12 Lattice Signature  

## Digital Signature conti.  

### Sigma protocol for average hard NP relation to ID scheme security  

Reduction by rewinding  
Suppose $Adv$ breaks ID scheme security with advantage $\frac{1}{n^c}$, we can construct a reduction $R$ that breaks the average hard NP relation.  
如果能夠用同樣的 commit 叫 $Adv$ 兩次，就能用 special soundness 的 Ext 來找出 witness。  
所以需要 rewinding，因為 $Adv$ 是一個 PPT algorithm，假設它由兩部分組成，且隨機性是給定的，因此變成 deterministic：  
$$  
P_1^*(x;r)=x,r,Com  
$$  
$$  
P_2^*(x,Ch;r)=Resp  
$$  

用 good $(x,r)$: $\Pr[Adv\text{ wins}|\text{input }(x,r)]\ge \frac{1}{2n^c}$  
$\Pr[\text{good }(x,r)]\ge \frac{1}{2n^c}$  

### Fiat-Shamir transformation in ROM  

Given RO $H$, we can construct a Signature scheme from an ID scheme. In other words, suppose there's an $Adv$ that breaks the EUF-CMA of the transformed signature scheme(acts as a Prover), we can construct a reduction $R$ that breaks the ID scheme.  
$Adv$ is given access to a RO $H$ and a signature oracle $Sign_{sk}$, $R$ simulate them by:  
* RO: lazy sampling  
* $Sign_{sk}$: use $Trans_{sk}$ oracle.  

The key problem is that we need to answer to an interactive transcript but the $Adv$ can only generate a fixed transcript. So, a trivial solution doesn't work, and we have to generate a $Com$ earlier.  

The method is similar to that of FO transformation. Since $Adv$ wins if $ch^*=H(Com^*,m^*)$, it very likely needs to query $H$ for the the $ch^*$. So $R$ sends one $com$($i^*\gets[q_H]$) from the queries of the $H$ and set the result to be $ch$ from $Ch$.  
## Lattice-based Signature  

### SIS(Short Integer Solution) assumption  

| Ch                                            |                        | Adv |  
| --------------------------------------------- | ---------------------- | --- |  
| $A\overset{\$}\gets \mathbb{Z}_q^{n\times m}$ | $A$->                  |     |  
| wins iff $Av=0 \mod q$                        | <-$v\in\mathbb{Z}_q^m$ |     |  

Additional requirements:  
* trivially, $v\ne 0$  
* $v$ 很短，$\|v\|_2\le \beta$  

This can be reduced to Lattice problems that are proven to be NP-hard.  

$n$ is the security parameter, $m$ should be sufficiently large(so that there's a solution), $q$ is a modulus(suff. large), $\beta$ is the shortness parameter. $q>\beta\cdot \textsf{poly}(n)$  

不只找到 $Av=0$ 是 hard，找到隨便一個 $Av=t$ 也是 hard。  
**Informal notes**:  
Prover works in plaintext space, Verifier works in the ciphertext space.  

### Compare to Schnorr signature scheme(sigma protocol, based on DL assumption)  

(use non-homogeneous SIS)  
* Hide $sk$ and send $pk$  
  * DL hides $s$ in $pk=g^s$.  
  * SIS hides $s$(short) in $t=As$.  
* Sigma protocal $(com,ch,resp)$  
  * DL:  
$k\gets \mathbb{Z}_q$, $com=r=g^k$->  
<-$ch=c\in\mathbb{Z}_q$  
$resp=z=k-sc$->  
  * SIS:  
$k\gets\mathcal{D}_\sigma^m$, $com=Ak$->(discrete Gaussian)  
<-$c=\begin{bmatrix}-d,\ldots,d\end{bmatrix}$  
$resp=z=k-cs$->  
accept iff $Az=r-c(As)$ and $z$ is short  

However, the SIS Sigma protocol is not a sigma protocol (no special soundness, no HVZK). So, we need to make a version with abort and achieve a type 1 ID scheme.  

### ID scheme from SIS  

$(Gen,P_1,P_2,V)$  
* $Gen(1^n)$  
  * $A\overset{\$}\gets\mathbb{Z}_q^{n\times m}$  
  * $s\gets\begin{bmatrix}-d,\ldots,d\end{bmatrix}^m$  
  * $pk=(A,t=As),sk=(A,s)$  
* $P$ and $V$: as in the comparison part  

**Reduction**:  
Use a similar special soundness argument.  
Suppose a $Adv$ breaks the ID scheme, we can construct a reduction $R$ that breaks the SIS assumption.  
$R$ samples a $s$ by himself and send $t=As$. $Adv$ similarly supports rewinding. So $R$ queries for a same $com=r$ and get $(c_1,z_1),(c_2,z_2)$, such that $Az_1=r-tc_1$ and $Az_2=r-tc_2$.  
Therefore, $R$ can get a $v$ by:  
$$  
\begin{align*}  
A(z_1-z_2)&=-t(c_1-c_2)\\  
&=-As(c_1-c_2)\\  
A(z_1-z_2+s(c_1-c_2))&=0  
\end{align*}  
$$  
So $R$ can simply outputs $v=z_1-z_2+s(c_1-c_2)$.  
A problem is that $v$ may not be short and $v$ maybe 0.(ignore this)  
Another problem is that multiple $s$ may correspond to the same $t$. Somehow this can be solved.  

### HVZK  

Simulate 出來的 $(com,ch,resp)=(r,c,z)$ 要 hide $k$，否則無法在不知道 $k$ 的情況下 simulate 出來。  
但 SIS-based $z=k-sc$ 中，$k$ 是 mean 0 的 discrete Gaussian，所以 $z$ 相當於被平移 $sc$，所以 $z$ 可能包含一些 $k$ 的資訊。  
解決的關鍵：with abort version。  

# week 13 Zero Knowledge  

$\Sigma$-protocal for $R_{DL}$(honest verifier)  
* Prover has $(s,g^s)$, Verifier has $(G,g,g^s)$  
* Prover samples $k\gets\mathbb{Z}_q$  
* Prover sends $r=g^k$  
* Verifier sends $c\gets\mathbb{Z}_q$  
* Prover sends $z=k-sc$  
* Verifier checks if $g^z=r(g^s)^{-c}$  

For some dishonest verifier, it may get $k$ from $r=g^k$, and sends $c=k$. Therefore it can know $s$ from $z$. 這個互動過程就無法 simulate，因為 $k$ 決定後， $z$ 就會被 $s$ 決定，但 $Sim$ 不知道 $s$。  

## definition of ZK  

A interactive protocal $(P,V)$ for a NP relation R is ZK if $\forall(x,y)\in R$, $\forall \text{PPT } V^*, \exists Sim s.t.$ the interaction of $(P,V^*)$ and the output of $Sim$ is computationally indistinguishable(or statistically indistinguishable).  
可以互動很多次  

## NP language  

For an NP language L, $\exists$ polynomial time $V$ s.t. $\forall x\in L, \exists$ witness $w$ s.t. $V(x,w)=1$. And $\forall x\not\in L, \forall$ witness $w$ $V(x,w)=0$.  

### example 3 coloring  

$L_{G3C}=\{G=(V,E)|\text{G is 3 colorable}\}$  
$L\in NP$, witness is a map $\phi:V\to {1,2,3}$  

### ZK for NP language L  

互動多次 $\langle P(w), V\rangle(x)$  
* Completeness: $\forall x\in L$ and a valid witness $w$, $\Pr[\langle P(w), V\rangle(x)=\text{accept}]\ge 1-negl(|x|)$  
* $\epsilon$-soundness: 壞人 prover 不能說服 verifier。$\forall$ malicious $P^*$, $\Pr[\langle P^*, V\rangle(x)=\text{accept}]\le \epsilon(|x|)$  
  * If only for PPT $P^*$, comp. soundness  
  * If for unbounded $P^*$, stat. soundness  
* ZK: $\forall$ malicious $V^*$, $\exists Sim$ s.t. $V^*$'s view from $\langle P(w), V^*\rangle(x)\approx Sim(x)$  
  * $V^*$ 必須是 PPT，不然自己就知道 witness，$Sim$ 也是一樣的道理  
  * 但兩個分布不可區分可以是 comp. 或 stat.  

## commitment scheme  

$Com=(C,R)$, committer(sender) and receiver  
直覺理解: committer 傳送放在箱子裡的 m，receiver 不能打開，但在驗證階段(reveil phase)，committer 把鑰匙給 receiver，receiver 可以驗證當初傳的確實是 m。  
* Binding: 不同的 m 對應到不同箱子  
* Hiding: 只看到箱子不知道裡面裝什麼  

正式定義:  
* Commit phase: C sends c to R(with decommitment d, maybe random tape)，可以很多次  
* Reveil phase: C sends m,d to R, open(m,c,d)=acc/rej  
* Binding: $\forall$ adversary as malicious C, it wins iff $open(m_0,c,d_0)=open(m_1,c,d_1)$=accept. $\Pr[\text{it wins}]$ is negligible.  
* Hiding(IND-based): 對於任何兩個 messages $m_0,m_1$, $\forall R^*$ 的 $view(\langle C(m_0),R^*\rangle)\approx_c view(\langle C(m_1),R^*\rangle)$  

一樣 binding, hiding 都有可能是 PPT 或 unbounded。但是不能兩個都 unbounded(left as exercise)  

### A construction from OWP  

For a OWP $f$ with its hardcore predicate $h$, we can construct a commitment scheme for 1 bit.  
$Com(b), b\in\{0,1\}$  
* sample $r\gets\{0,1\}^n$  
* output $c=(f(r),h(r)\oplus b)$, keep $d=r$  

$open(b,c,d)$  
* acc iff $c=(f(d),h(d)\oplus b)$  

這會是 stat.(perfect) binding，因為一個 adversary 想找出 $(c_0=0,d_0), (c_1=1,d_1)$，但是 $d=r$ 決定後，$f(r)$ 和 $h(r)$ 都決定。  
comp. binding，因為如果能區分 $c_0, c_1$ 會 break HC，而 unbounded adversary 可以直接算出 $r$ 再算 $h(r)$。  

## ZK protocol for $L_{G3C}$  

[Related material](https://www.cs.cmu.edu/~goyal/s18/15503/scribe_notes/lecture23.pdf)  

用一個上面的 commitment scheme  

$P(G,\phi)$  
* $\pi\gets S_3$, 三種顏色隨機的排序  
* $\psi=\pi(\phi)$  
* $\forall v\in V, (c_v,d_v)\gets Com(\phi_v)$  
* sends $Com(\phi)$  

$V(G)$  
* $e\gets E$  
* sends $e=(u,v)$  
* gets $\psi_u,d_u,\psi_v,d_v$  
* accept iff $open(\psi_u,c_u,d_u)\land open(\psi_v,c_v,d_v)\land \psi_u\ne\psi_v$  

Security  
* Completeness: yes  
* Soundness: $(1-\frac{1}{|E|})$-soundness  
* ZK  
$V^*$ 的 view 是 $(G,com(\psi),V^*(com(\psi))=e=(u,v),\psi_u,d_u,\psi_v,d_v)$  
對於一個圖 $G$，$Sim$ 隨便找一個邊亂塗不同顏色，其他點甚至可以都塗一樣的顏色，造出 $\psi'$，期待 verifier 剛好問到那條邊。如果不是的話，就 rewind 多試幾次。  
直覺想為何 comp. indis.: $com(\psi')$ 如果與真正沒亂塗的 commitment 可分辨會 break commitment scheme 的 hiding。$\psi'_u,d_u,\psi'_v,d_v$ 是真的從 commitment 來的，所以好像也沒問題。  

Hybrid argument: 從有 witness 的 $Hyb_{real}$ 到沒有 witness 的 $Sim$  
* $Hyb_{real}$: 原本的定義  
* $Hyb_1$: 指定一條邊 $e'$，若 $e\ne e'$ 就 rewind。  
因為邊 $e'$ 還是隨機的，所以 view 的分布一模一樣。  
* $Hyb_2$: 把 $\psi$ 改得與 $\psi'$ 近一點。與 real 一樣 $\psi=\pi(\phi)$, $\psi'_u=\psi_u, \psi'_v=\psi_v$，但 $\psi'_w$ 隨便塗一個顏色(1)。  
view 裡的 $\psi$ 都改成奇怪的 $\psi'$，所以被改掉的只有 $com(\psi)$，裡面被改掉了很多點的 color。偷懶的講法: $Hyb_1$ 到 $Hyb_2$ 中間可以再有很多 hybrids，慢慢把 $\psi_w$ 改掉。如果能 break 的話就會 break commitment scheme 的 hiding。  
<!-- 待補 -->  

# week 14 Fully Homomorphic Encryption  

