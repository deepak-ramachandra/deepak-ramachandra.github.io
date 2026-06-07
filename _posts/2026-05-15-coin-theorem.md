---
title: "A Story Among My Scratches"
date: 2026-05-15
categories: [Math]
tags: [theorem]
math: true
image:
    path: /assets/img/IMG_5832_sq.jpeg
    alt: Every once in a while, in a period of time that feels long and filled with exhaustion, though very rarely, you might see something like this. Just thinking about it gets your heart racing, and you can feel your confidence coming back. After a long and strenuous climb to the top, it serves as the foothold that you desperately needed. It is not a miracle, maybe it's one out of a hundred, or even one out of a thousand, but it's the one you went to reach and managed to grab. By grabbing and connecting these rare moments, you are able to keep climbing higher and higher.— Fuki Hibarida, (Haikyuu!!)
---

My Master's thesis was about proving the [Differential Privacy]({% post_url 2026-05-16-differential-privacy %}) of Thompson Sampling[^agrawal2017] for two arm bandits. Calculating expectations of random variables was well known to me, but the progression of my Master's thesis demanded from me the skill of proving high probability bounds, which in turn demanded a deeper knowledge of the underlying distribution.

While deriving upper bounds for the privacy loss of Thompson Sampling, I was stuck with an expression without a direction to pursue. I needed an intermediate foothold from where I could proceed to the solution intuitively. After making many attempts I finally succeeded in bounding the privacy loss. Looking back in my scratches, I find that the key result that solidified my intuition won't make it into my final draft. I have submitted the full work to [Neurips 2026](https://neurips.cc/) and awaiting a decision. I plan to link it here soon. Unlike the many rare footholds I managed to grab that contributed to the final result, this one finds its place here in the post. The inspiration and the theory of the Coin Theorem is developed here.


## Background
<div style="display:none">
$$\newcommand{\p}{\mathcal{P}}$$
$$\newcommand{\coloneqq}{:=}$$
$$\newcommand{\I}{\mathbb{1}}$$
$$\newcommand{\E}{\mathbb{E}}$$
</div>

During 2022, when I worked at [MakeMyTrip](https://makemytrip.com/), I was working on the Single Hotel Search project[^yadav2022]. We had four different recommendation systems at our disposal and had to comparatively evaluate each of their Click Through Rate (CTR) and Conversion Rate (CR). A straightforward method would be to randomly split the upcoming month's incoming traffic into four parts and serve one model to all users in each part. Then we could evaluate CTR and CR for every model. However, this exploratory endeavor to find the best model results in the organization bearing some revenue loss during this month's time: obviously three fourths of the month's traffic was not served by the optimal model.

We reported metrics for every user cohort (e.g. new users, 4-5 star bookers, others grouped by city: Bangalore, Delhi; and so on). But for simplicity assume every user identical and independent. At each time we have to decide which model to use to recommend hotels on the listing page right below the hotel they searched for. Based on the recommendations of the model (and other factors of the user beyond our control) the user decides to click on and/or book the hotel. We only know how good the choice of the model (used in the recommendation system) is only after we observe enough clicks and books. However, dwelling on a bad choice leads to regret. Essentially, a natural question to ask is:

>While figuring out which of these recommendation systems is optimal, how do we also minimize the revenue loss we bear due to serving hotel recommendations from non-optimal (other) systems?

The action/arm refers to the model we choose to serve recommendations from and the reward refers to whether or not the user ends up booking any hotel in that login session after seeing the recommended hotel list (0/1 reward). As a result, the average reward (unknown) of each action thus refers to the conversion rate of that recommendation system. Turns out, there is a well formulated problem related to this.

### Multi-Arm Bandit Problem
We consider here the classical stochastic multi-arm bandit setting. The game is played over a horizon of $T$ steps. At each step, $t=1\ldots T$, the agent is allowed to choose an arm $a_t \in \\{1,2,\ldots, N\\}$. The environment $\mathcal{E}$ provides a stochastic reward $r_t(a_t) \in [0,1]$ only based on the choice of $a_t$ at the current step, independent of past history or the step number $t$. However this distribution is unknown to the algorithm. Suppose the expected rewards for the arms are $\mu_a$, $a=1\ldots N$ respectively. Let $\mu^\star = \max_{a} \mu_a$. The goal of any agent $\mathcal{A}$ is to minimize pseudo regret $R(T)$:

$$
\mathrm{R(T)} = T\mu^\star - \sum_{t\leq T}\mathbb{E}\left[\mu_{A_t}\right],
$$

where the expectation is given by the probability distribution over the agent's actions and the distribution over the rewards generated by $\mathcal{E}$. The agent observes the reward only for the action it takes and must utilize its past actions and realized rewards to play competently.

For illustration, let us go back to the recommendation system problem: assume the CR of the four models to be $2,1.5,1.7,$ and $1.2\\%$ resp. This information is totally (not even a clue) unknown to us at the start of the experiment, hence we have to serve at least a few users just to get an estimate. If we adopted the straightforward method of serving the traffic of $T$ different users with 4 options in a uniformly random fashion, the pseudo regret would be:

$$
R(T) = \frac{T}{100}\left(\frac{2-1.5}{4} + \frac{2-1.7}{4} + \frac{2-1.2}{4}\right) = \frac{T}{250} = \mathcal{O}(T)
$$

We circle back to the same question:

>While figuring out which of these choices is optimal, how do we also minimize the loss we bear due to non-optimal (other) choices?
{: .prompt-warning}


Since the agent does not know the conversion rate, it must use the empirical estimate: CR among users served until now as a proxy to evaluate which model is better. Naturally, in order to be sure about these estimates, the agent needs to serve recommendations from every model sufficiently many times, so the empirical estimates are very likely to be near the true CR value. As such, the agent needs to balance the urge to only choose the action with the best estimate (exploitation) and the urge to improve the quality of the estimates by trying out all choices (exploration). This is called the exploration-exploitation dilemma. Finally, based on how sure the agent is about the estimates, it can dial down how often it serves users with recommendations from suboptimal models.

There are two main algorithms that solve this problem with logarithmic regret, namely Upper Confidence Bound (UCB) and Thompson Sampling (TS). If the gaps of mean between the best and the sub-optimal choice is $\Delta_a$, for the $N$ choices problem, both achieve the best possible regret:

$$\Delta_a = \mu^\star-\mu_a, \quad R(T) = \mathcal{O}\left(\sum_{\Delta_a\neq 0}\frac{\log T}{\Delta_a}\right)$$

It is shown that we cannot do better than this. If $\Delta_a$ is very small, we can show the regret is $\sqrt{NT\log T}$, not arbitrarily large. In particular, my advisor [Prof. Shipra Agrawal](https://www.columbia.edu/~sa3305/) showed this result for TS [^agrawal2017]. For our post, we discuss only TS.

### Thompson Sampling
The Thompson Sampling algorithm (TS) for multi-arm bandits maintains a posterior belief about the true mean reward of every arm based on its empirical mean and its pull counts. We define them below.

$$
n_a(\tau) = \sum_{t \leq \tau} \mathbb{1}(A_t = a) \qquad
\hat\mu_a(\tau) = \frac{\sum_{t \leq \tau} \mathbb{1}(A_t=a) r_t}{n_a(\tau) + 1}
$$

<small>
Note that we divide by $n_a + 1$ to avoid zero division, yet we call it empirical mean for ease.
</small>

TS algorithm believes that the true mean $\mu_a$ is close to the empirical estimate $\hat\mu_a$, but the uncertainty is inversely proportional to how many rewards were used to construct the estimate - ie., uncertainty $\propto \frac{1}{n_a + 1}$. Given $n_a(t-1)$, the estimate $\hat\mu_a(t-1)$ of bounded rewards is approximately Gaussian with mean $\mu_a$ by the central limit theorem (CLT). Rewards are independent and lie in $[0,1]$, so each has variance less than $1$. As a result, the variance of the estimate $\hat\mu_a(t-1)$ is less than $\frac{1}{n_a(t-1) + 1}$. However, instead, we have the estimate $\hat\mu_a$ and the count $n_a$. With no other prior belief about $\mu_a$, TS uses the heuristic based on available data and flips the CLT into a belief. That is, given the data,

$$\mu_a \sim \mathcal{N}\!\left(\hat{\mu}_a(t-1),\, \frac{1}{n_a(t-1)+1}\right)$$

With this, TS samples $\theta(t)$ from this above distribution, and plays the arm with the highest $\theta_a$. The randomness in sampling naturally gives rise to exploration.



>**Thompson Sampling with Gaussian Priors**<br>
>**Initialize:** For each arm $a = 1, \ldots, N$, set $n_a(0)=0$, $$\hat{\mu}_a(0) = 0$$ . <br>
>**for** $t = 1, 2, \ldots, T$ **do**<br>
>&emsp;**for** each arm $a = 1, \ldots, N$ **do**<br>
>&emsp;&emsp;Sample $$\theta_a(t) \sim \mathcal{N}\left(\hat{\mu}_a(t-1),\, \frac{1}{n_a(t-1)+1}\right)$$ <br>
>&emsp;**end for**<br>
>&emsp;Play $$A_t \in \mathrm{Argmax}_a\, \theta_a(t)$$, observe reward $$r_t$$ <br>
>&emsp; $$\hat{\mu}_{A_t}(t) \leftarrow \dfrac{\hat{\mu}_{A_t}(t-1)\,(n_{A_t}(t-1)+1)+r_t}{n_{A_t}(t-1)+2}$$ <br>
>&emsp; $n_{A_t}(t) \leftarrow n_{A_t}(t-1)+1$<br>
>**end for**
{: .prompt-tip}

An arm is likely to be played if it has a large $\hat\mu_a$, or a small $n_a$ (due to high standard deviation, the sampled $\theta_a$ could be larger regardless of $\hat\mu_a$).

The original project [^yadav2022] I was a part of at MakeMyTrip used a Contextual Bandits version of TS. It led to a 1.5%-2% lift in overall conversion, but more importantly 20% lift for cases where the searched hotel was sold out, since it was better at recommending alternatives.

I came to Columbia with the sole intention of starting research in Safe Reinforcement Learning. My plan was to start with theoretical research to solidify my mathematical intuition before setting foot in anything empirical. Since I believe in starting with fundamentals, and given my background in bandits I sought out Prof. Agrawal's guidance. I proposed to work with her on a project with the goal of solving the open problem on the complexity of Joint Differential Privacy in linear contextual bandits[^azize2024]. After exploring this problem as a part of the course project, she generously agreed to advise my Master's Thesis. I took up the studying the differential privacy of Thompson Sampling for the two arm bandit setting. This is how I began my journey of Safe RL research.

### Differential Privacy
Differential Privacy (DP) is a property of any randomized algorithm that takes a database with every row corresponding to one user's data as input. The extent of privacy is governed by the extent to which output distribution can change when one user's data is replaced or omitted. In a two-armed bandit setting with finite horizon $T$, without loss of generality, we can consider the rewards to be pre-sampled and the algorithm to sequentially process them. Thus rewards can be considered to be the input and the actions can be considered as random outputs.

For the current setting, two reward sequences $R, R^\prime \in [0,1]^{T\times2}$ are called neighboring if and only if they differ at exactly one time step $t \in [T]$. Fixing the input reward sequence $R \in [0,1]^{T\times2}$, the algorithm outputs a random action sequence $a_{1:T} \in \Omega$, and we denote the resulting categorical distribution over $\Omega = \\{1,2\\}^T$ by $\p_R(\;\cdot\;)$. If instead we set the input to $R^\prime$, the same sample space $\Omega = \\{1,2\\}^T$ is measured by a different law $\p_{R^\prime}(\;\cdot\;)$.


>Thompson Sampling would be called $(\epsilon,\delta)$-DP if and only if, for every pair of neighboring reward sequences $R,R^\prime$ and every action sequence $a_{1:T} \in \Omega$:
>
> $$\p_{R}(A_{1:T} = a_{1:T}) \leq e^\epsilon\;\p_{R^\prime}(A_{1:T} = a_{1:T}) + \delta$$
{: .prompt-tip}

We show that showing a high probability bound on privacy loss is a sufficient condition in [another post]({% post_url 2026-05-16-differential-privacy %}). Essentially, we define privacy loss function:

$$
\ell_{R,R^\prime}:\Omega \rightarrow \mathbb{R},\quad \ell_{R,R^\prime}(a_{1:T}) = \log\frac{\p_{R}(A_{1:T} = a_{1:T})}{\p_{R^\prime}(A_{1:T} = a_{1:T})}
$$

And a well-known sufficient condition to argue that TS is $(\epsilon,\delta)$-DP would be to show that the corresponding random variable $\mathcal{L}\_{R,R^\prime} = \ell\_{R,R^\prime}(A_{1:T}),$ where $A_{1:T} \sim \p_R(\;\cdot\;)$ is bounded with high probability as follows.

$$
\p_{R}\bigl(\mathcal{L}_{R,R^\prime} \geq \epsilon\bigr) \leq \delta
$$


## Setup
For the two-arm bandit case, my method involved exploiting the closed form probabilities of TS to analytically bound the privacy loss random variable. Since the algorithm operates sequentially, we can write the privacy loss as a sum via the chain rule:

$$\mathcal{L}_{R,R^\prime} = \sum_{t \leq T}\log\frac{\p_R(A_t|A_{1:t-1})}{\p_{R^\prime}(A_t|A_{1:t-1})}$$


Specifically for the two arm setting, define:

$$
\begin{align*}
\hat\Delta(t) &:= \hat\mu_1(t) - \hat\mu_2(t)\\
\frac{1}{k(t)} &:= \frac{1}{n_1(t) + 1} + \frac{1}{n_2(t) + 1}
\end{align*}
$$

The main advantage of working with the two arm case is that we get a closed form for the action probabilities. We play action 1 if $\theta_1 - \theta_2 > 0$ or we play action 2 otherwise. Since the scores are independent of each other,

$$
\theta_1(t) - \theta_2(t) \sim \mathcal{N}\!\left(\hat\Delta(t-1), \frac{1}{k(t-1)}\right)\\
$$

As a result, we get the following closed forms for the action probabilities, as a function of the history.

$$
\begin{align*}
\p_R(A_t=1|A_{1:t-1}) &= \p_R\left(\theta_1(t) - \theta_2(t)\geq 0\right)\\
&=\Phi\left(\sqrt{k(t-1)}\hat\Delta(t-1)\right),\\
 \p_R(A_t=2|A_{1:t-1}) &= \Phi\left(-\sqrt{k(t-1)}\hat\Delta(t-1)\right)\\
 \therefore \p_R(A_{1:T} = a_{1:T}) &= \prod_{t\leq T}\p_R(A_t=a_t|A_{1:t-1} = a_{1:t-1})
\end{align*}
$$

where $\Phi$ refers to the cdf of standard gaussian, and later we use $\phi$ to denote the density. And similar situation for $\p_{R^\prime}$.

$$
\begin{align*}
\hat\Delta^\prime(t) &:= \hat\mu^\prime_1(t) - \hat\mu^\prime_2(t)\\
\implies \p_{R^\prime}(A_t=1|A_{1:t-1}) &= \Phi\left(\sqrt{k(t-1)}\hat\Delta^\prime(t-1)\right),\\
 \p_{R^\prime}(A_t=2|A_{1:t-1}) &= \Phi\left(-\sqrt{k(t-1)}\hat\Delta^\prime(t-1)\right)
\end{align*}
$$

Note that $n_1,n_2$ and $k$ depend only on the action sequence $a_{1:t}$ and not on the rewards.

## The Crux of the Climb
Suppose at time $t^\prime$, we played arm 2 and its reward was changed, $\p_R$ and $\p_{R^\prime}$ would differ only because of their corresponding $\hat\Delta$. Bounding involved working with many cases. The worst one is presented here.  $\hat\Delta$s would differ by at most $1/(n_2(t-1) + 1)$ at every time $t$. Also, suppose from now onwards, $\sqrt{k}\hat\Delta > 1$. That is, arm 1 has a greater chance of getting played under $\p_R$. The privacy loss can be upper bounded:


$$
\begin{align*}
\mathcal{L}_{R,R^\prime} \;&\leq\; \sum_{t \leq T} \frac{1}{n_2(t-1) + 1}\;\frac{d\;}{dr_{t^\prime}}\bigl(\log \p_R(A_t|A_{1:t-1})\bigr)\\
&\leq\sum_{t \leq T} \frac{\sqrt{k(t-1)}}{n_2(t-1) + 1} \frac{\phi\left(\sqrt{k(t-1)}\hat\Delta(t-1)\right)}{\p_R(A_t|A_{1:t-1})}\\
&\leq\sum_{t \leq T} \left(\frac{1}{\sqrt{n_2(t-1) + 1}}\right) \frac{\phi\left(\sqrt{k(t-1)}\hat\Delta(t-1)\right)}{\p_R(A_t|A_{1:t-1})}\\
&=\sum_{t \leq T} \left(\frac{1}{\sqrt{n_2(t-1) + 1}}\right) f(t), \quad\text{let $f(t) := \frac{\phi(\ldots)}{\p_R(\ldots)}.$}
\end{align*}
$$

In our discussion this action $2$ has the lower probability. If it is not played, $n_2$ will not increment and regardless of bounding $f(t)$, we can only assure a trivial bound of $\mathcal{O}(T)$. In this sense, we can decompose the sum into two parts, the former contains indices where arm 2 is played and the latter contains where it is not:

$$
\begin{align*}
\mathcal{L}_{R,R^\prime} \;&\leq\; \sum_{t \leq T} \left(\frac{\I(A_t=2)}{\sqrt{n_2(t-1) + 1}}\right) f(t) + \sum_{t \leq T}\left(\frac{\I(A_t=1)}{\sqrt{n_2(t-1) + 1}}\right) f(t)
\end{align*}
$$

Along the first sum, we have $n_2$ steadily incrementing. However, we have that

$$\I(A_t=2)f(t) = \frac{\phi\left(\sqrt{k(t-1)}\hat\Delta(t-1)\right)}{\p_R(A_t=2|A_{1:t-1})} = \frac{\phi\left(\sqrt{k(t-1)}\hat\Delta(t-1)\right)}{\Phi\left(-\sqrt{k(t-1)}\hat\Delta(t-1)\right)}$$

Now, we end up with:

$$\forall t \in [T],\quad \I(A_t=2)f(t) \le 2\sqrt{k(t-1)}\hat\Delta(t-1)\leq \sqrt{\log(T/\delta)}\quad\text{w.p.}\quad1-\delta$$

The first inequality is from Mills', and the second inequality is just from the fact that if $\sqrt{k}\hat\Delta$ was too large, arm 2 would not have been played. Leading to

$$\sum_{t \leq T} \left(\frac{\I(A_t=2)}{\sqrt{n_2(t-1) + 1}}\right) f(t) \leq 2\sqrt{T\log(T/\delta)}\quad\text{w.p.}\quad1-\delta$$

For the other sum along the indicator $\I(A_t=1)$, we are just waiting for $n_2$ to be incremented. The sum depends pretty much on the totals accumulated between every play of arm 2. To show this, let $\tau_j$ refer to the time index when this second arm was played for the $j$th time. So the remaining sum can be written as:


$$
\sum_{t \leq T} \left(\frac{\I(A_t=1)}{\sqrt{n_2(t-1) + 1}}\right) f(t) = \sum_{j=1}^{n_2(T)} \frac{1}{\sqrt{j + 1}}\left(\sum_{t=\tau_j}^{\tau_{j+1} - 1}\I(A_t=1)f(t)\right)
$$


Define

$$Y(j) = \sum_{t=\tau_j}^{\tau_{j+1} - 1}\I(A_t=1)f(t)$$

With $n_2(T) \leq T$, we end up with

$$
\begin{equation}\label{eq:loss}
\mathcal{L}_{R,R^\prime} \leq 2\sqrt{T\log(T/\delta)} + \sum_{j=1}^{T} \frac{Y(j)}{\sqrt{j + 1}}
\end{equation}
$$

Essentially, we are incurring a privacy loss of $Y(j)$ between the two plays of arm 2. The denominator does not advance until the second arm (whose probability is low) is played. In the worst case the second arm is almost never played and we might end up with a trivial upper bound of $\mathcal{O}(T)$.

<blockquote class="prompt-warning">
By reverse engineering, it is quite clear that if I show

$$\forall j \in [T],\quad Y(j) \leq \sqrt{\log(T/\delta)}\quad\text{w.p.}\quad1-\delta,$$

I could obtain

$$\mathcal{L}_{R,R^\prime} = \mathcal{O}\left(\sqrt{T\log(T/\delta)}\right)\quad\text{w.p.}\quad1-\delta,$$

The goal now becomes to obtain a (sqrt of) logarithmic bound on every Y.
</blockquote>


## Conjuring an image of happiness
For the suboptimal arm 2, its probability of playing is low as per Thompson Sampling. As we go towards the end of the time horizon $T$, its probability will be negligible. Given that $Y = \sum_{\tau_j}^{\tau_{j+1}} I(A_t=1)f(t)$, we continue with unravelling $f(t)$ with the condition that $A_t=1$:

$$
\begin{align*}
    I(A_t=1)f(t) &= \frac{\phi(\sqrt{k}\hat\Delta)}{\p(A_t=1|A_{1:t-1})}\\
    &\leq 2\;\phi(\sqrt{k}\hat\Delta)\\
    &\propto \Phi(-\sqrt{k}\hat\Delta) = \p(A_t=2|A_{1:t-1})
\end{align*}
$$

The proportionality follows from the Mill's inequality, which states that the density and the cdf are closely related to each other for a normal distribution.

>About, $Y(j) := \sum_{\tau_j}^{\tau_{j+1}} I(A_t=1)f(t)$, we conjecture two things about $f(t)$ when $A_t=1$.
>1. <p>$f(t) \propto P(A_t=2|A_{1:t-1})$</p>
>2. <p>$\sum_{\tau_j}^{\tau_{j+1}} I(A_t=1)P(A_t=2|A_{1:t-1}) \leq \sqrt{\log(T/\delta)}\quad\text{w.p.}\quad1-\delta$</p>
{: .prompt-warning }

## Outlines
<div>I worked my way backwards. I did not want to work on the first conjecture unless I proved the second anyways. We first try for the case when the $\p(A_t=2|A_{1:t-1}) = p$ is fixed throughout. Then $\sum_{t=\tau_j}^{\tau_{j+1} - 1}\p(A_t=2|A_{1:t-1}) \sim \mathrm{Geom}(p)$. The following lemma is not used in the main result of this post, but serves as inspiration.</div>

>**Lemma 1:** Let $X_1, X_2, \ldots \overset{\text{iid}}{\sim} \mathrm{Bernoulli}(p)$ with $p \in (0,1)$, and let $\tau = \min\\{k : X_k = 1\\}$ be the first time we toss a success. Then
>
>$$p\tau< \log(1/\delta)\quad\text{w.p.}\quad 1 - \delta.$$
{: .prompt-info }

**Proof.**
Since the tosses are iid,

$$\p(\tau > k) = \p(X_1=0,\ldots,X_k=0) = (1-p)^k < e^{-pk}.$$

We use the standard inequality $1 - p < e^{-p}$, with $p \in [0,1]$ here.

Thus, we end up with

$$
\p(\tau \leq k) \geq 1 - \exp(-pk)
$$

Setting $k = \log(1/\delta)/p$, we get the required result.

---

>However, what if the bias (although predictable) was changing with time? This precisely describes our problem: playing arm 1 modeled as tossing tails and playing arm 2 as tossing heads. The score is the total accumulated bias throughout this run. The freedom to consider any reward sequence is modeled as the freedom to choose the bias of the coin before every toss.
{: .prompt-info}


## Game

Most of the work poured into the main proof involved different approaches and iterations. Among many pages of scratches, the theorem developed in this post sat close to my heart. This is the first high probability bound I ever formulated and worked on. This result turned out to provide a valid, illustrative, intermediate goal that gave me the confidence for the development of the algebra of my thesis.  Unfortunately, it will not make it into the final draft, but it finds its place on the web. My original proof exploits a key pattern in the game, whereas Claude Code gave a totally different, slick proof and hopefully a great read.
Suppose you are given the liberty to set the bias of coin to whatever value $b_t \in (0,1)$ before you toss it. Every time you toss a tail, you get some score. However, if you toss a head, the game is over. The score you get is equal to the bias $b_t$ of the coin you just tossed.

Let $\tau$ be the first time we toss heads. That is, we toss this coin $\tau$ times.

$$\tau = \min\{t \mid X_t=1\}$$

Define $Y$ as the sum of biases until we toss heads for the first time. That is:

$$Y \coloneqq \sum_{t=1}^{\tau-1} b_t$$

So if you choose to be greedy and set the bias of the coin to be $>0.5$, you will most likely toss heads and the game ends right away. On the other hand if you set the bias to be $<0.1$, you will likely toss many tails in a row, and even then the total score might be low. What is a high probability upper bound on the total score earned?


## Theorem

<blockquote class="prompt-info">
<strong>Theorem (Coin).</strong> Suppose we have a coin that changes its bias every time it is tossed. Let $X_t=1$ if the toss at time $t$ results in heads and $X_t=0$ if tails, and let $\mathcal{F}_t = \sigma(X_1, \ldots, X_t)$ be the natural filtration. Define $b_t$ as the conditional probability of heads given the past:
$$b_t \coloneqq \p(X_t=1 \mid \mathcal{F}_{t-1})$$ and assume $b_t \in (0,1)$ almost surely. Then, for any $\delta \in (0, 1)$, as per the above definitions:

$$Y \leq \log(1/\delta) \quad \text{w.p.} \quad 1-\delta$$

</blockquote>


### Original Proof

During the game, we observe $\tau-1$ tails and the last toss will be heads. $\tau$ is the key random variable here. $b_t$ maybe a predictable ($\mathcal{F}_{t-1}$ measurable) variable, but we are only adding it to our score only when the past has all tails. If we evaluate it for our concerned path (history containing only tails), we get a known quantity. Define it as $w_t$ instead.

$$w_t := \p(X_t=1|X_1=0,X_2=0,\ldots,X_{t-1}=0)$$

With this, we can define $Y$ as a deterministic function of $\tau$ as $Y = \sum_{t\leq \tau-1}w_t$. The randomness in $Y$ comes solely from the randomness of $\tau$. We define a function

$$
\begin{align*}
    S(T) &:= \sum_{t\leq T}w_t\\
    \text{with that we have,}\quad Y &= S(\tau - 1)
\end{align*}
$$

Here, note that $S$ is also a known function, not just predictable. Also, it is non-negative and strictly increasing. Define another known quantity $T^\star$, such that


$$
\begin{align*}
T^\star := \inf \{t \in \mathbb{N}: S(t) > \log(1/\delta)\}\\
\implies S(T^\star-1) \leq \log(1/\delta) < S(T^\star).
\end{align*}
$$

Now, if the set over which we take the infimum happens to be empty (everything about $S$ is deterministic), then clearly $Y \leq \log(1/\delta)$ with probability 1. Therefore, for the non-trivial case, $T^\star$ is finite. So, with $S$ strictly increasing, we have that $S$ is invertible. Therefore, bounding $Y$ and $\tau$ are essentially the same problem. With $Y = S(\tau - 1)$, we show equality of the following events.

$$\begin{align*}
\{\tau \leq T^\star\} &= \{S(\tau-1) \leq S(T^\star-1)\}\\
&= \{Y \leq \log(1/\delta)\}
\end{align*}
$$

Since $S$ is deterministic, and $w_t \in (0,1)$, we apply $1 - x \leq \exp(-x)$. We use chain rule to write it as a clean product:

$$
\begin{align*}
    \p\left(Y > \log(1/\delta)\right) = \p(\tau > T^\star) &= \p(X_1=0, X_2=0, \ldots,\;X_{T^\star}=0)\\
    &= \prod_{t\leq T^\star}\p(X_t=0| X_1=0, \ldots,\;X_{t-1}=0)\\
    &= \prod_{t\leq T^\star}(1-w_t)\\
    &\leq \exp(-S(T^\star))\\
    &< \exp(-\log(1/\delta)) = \delta.
\end{align*}
$$

<div style="text-align:right">
$\blacksquare$
</div>

> Originally, I had informally proved $\p(Y > u)\leq \exp(-u)$ and arrived at the same conclusion. I was fortunate enough to take Advanced Probability Theory class by Prof. Ioannis Karatzas during Fall 2025 to learn the terminology to lay down the proof like so.

---

### Claude's Proof
Define the cumulative sum of biases:

$$S_t \coloneqq \sum_{k=1}^{t}b_k,\quad \text{so,}\;S_0=0.$$

With $0 < b_t < 1$, and $b_t$ predictable, $S_t$ is strictly increasing and predictable.
Define a new sequence:

$$M_0=1,\quad M_t = \I(X_t=0)\exp(b_t)\;M_{t-1}.$$

Starting from $1$, we keep on multiplying $\exp$ of the bias when we toss tails. The moment we toss heads, we set the sequence to zero and we never change it thereafter. Thus $M$ is an absorbing process.

Clearly, $M_t$ is non-negative.
With $\E_t[.] := \E[.|\mathcal{F}_{t-1}]$, we have:

$$
\begin{align*}
\E_t[M_t] &= \E[\I(X_t=0)\exp(b_t)\;M_{t-1}|\mathcal{F}_{t-1}]\\
&= M_{t-1}\exp(b_t)\;\E[\I(X_t=0)|\mathcal{F}_{t-1}]\\
&= M_{t-1}\exp(b_t)\;\p(X_t=0|\mathcal{F}_{t-1})\\
&= M_{t-1}\exp(b_t)\;(1-b_t)\\
&\leq M_{t-1} \qquad \text{since $\exp(-x) \geq 1-x$}
\end{align*}
$$

Hence, $(M_t)_{t \geq 0}$ is a non-negative supermartingale.

Moreover, since $S_t$ is increasing, we get:

$$Y = \sum_{t < \tau} b_t = \sup_{t < \tau}S_t$$

$$\sup_{t \geq 0}M_t = \sup_{t < \tau} \exp(S_t) = \exp(\sup_{t < \tau} S_t) = \exp(Y)$$


Using Ville's inequality:

$$\p\left(\sup_{t \geq 0} M_t \geq a\right)\leq \frac{\E[M_0]}{a}.$$

and also $M_0=1$. This essentially boils down to:

$$\p(\exp(Y) \geq a) \leq \frac{1}{a}$$

Setting $a=1/\delta$, we get the required result.
<div style="text-align:right">
$\blacksquare$
</div>

---

## Connecting back
After factoring probability of the lesser arm, we end up with:

$$
\sum_{t=\tau_j}^{\tau_{j+1} - 1}f(t) = c\;\sum_{t=\tau_j}^{\tau_{j+1} - 1} \p(A_t=2|a_{1:t-1})\leq c\cdot \log(1/\delta)\quad\text{w.p.}\quad 1-\delta.
$$

This is the same structure as the coin game, where we are adding up the bias of the coin until we toss heads.

$$
\sum_{t=\tau_j}^{\tau_{j+1} - 1}f(t) \leq c\cdot \log(T/\delta)\quad\text{w.p.}\quad 1-\frac{\delta}{T}.
$$

And union bound over bad events, we get:

$$
\forall j \in [T] \quad \sum_{t=\tau_j}^{\tau_{j+1} - 1}f(t) \leq c\cdot \log(T/\delta)\quad\text{w.p.}\quad 1-\delta.
$$

Continuing from $\eqref{eq:loss}$, we get

$$
\begin{align*}
\mathcal{L}_{R,R^\prime} &\leq c\sqrt{T \log T} + \sum_{j=1}^{T} \frac{1}{\sqrt{j + 1}}\left(\sum_{t=\tau_j}^{\tau_{j+1} - 1}f(t)\right)\\
&\leq  c\sqrt{T \log T} + \sum_{j=1}^{T} \frac{\log(T/\delta)}{\sqrt{j + 1}} \quad \text{w.p.} \quad 1-\delta\\
&= \mathcal{O}\left(\sqrt{T}\log(T/\delta)\right) \quad \text{w.p.} \quad 1-\delta
\end{align*}
$$

And this would mean that TS is $(\epsilon,\delta)$-DP, with $\epsilon = \mathcal{O}\left(\sqrt{T}\log(T/\delta)\right)$. A month later, when my advisor and I were working on the lower bounds, we happened to come up with an improvement for the upper bound as well.

$$
\begin{align*}
\mathcal{L}_{R,R^\prime} &\leq C\cdot\sum_{t\leq T}\frac{\p(A_t=2|a_{1:t-1})}{n_2(t-1) + 1}\\
&= \mathcal{O}\left(\log T\log(T/\delta)\right) \quad \text{w.p} \quad 1-\delta,
\end{align*}
$$

using the same logic. However, this second iteration had negative terms and we had to use time-uniform bounds. As a result, the above coin theorem was not included in my thesis. Based on the form of inequalities I have in the main paper, my advisor suggested I use Freedman-style bounds prevalent in bandit papers [^beygelzimer2011]. All in all, I am very grateful for the continual guidance and support of my advisor Prof. Agrawal throughout my Master's thesis.

## Conclusion
This post gave a brief overview about Thompson sampling and Differential Privacy. It then gave a brief overview of the problem I got stuck at when bounding the privacy loss. This led to the development of the game and my proof. This post serves as a souvenir as I finish up my Master's thesis.


[^agrawal2017]: Agrawal, S., & Goyal, N. (2017). Near-Optimal Regret Bounds for Thompson Sampling. *Journal of the ACM*, 64(5), Article 30.

[^yadav2022]: Yadav, V., Ramachandra, D., & Narasimha. (2022). [Deep Contextual Bandits for Model Selection in Travel E-commerce](https://tech.makemytrip.com/deep-contextual-bandits-for-model-selection-774eec6e5603). *MakeMyTrip Engineering*.

[^azize2024]: Azize, A., & Basu, D. (2024). [Open Problem: What is the Complexity of Joint Differential Privacy in Linear Contextual Bandits?](https://proceedings.mlr.press/v247/azize24a.html) *Proceedings of the Thirty-Seventh Conference on Learning Theory (COLT)*, PMLR 247:5306–5311.

[^beygelzimer2011]: Alina Beygelzimer, John Langford, Lihong Li, Lev Reyzin, and Robert E. Schapire. “Contextual bandit algorithms with supervised learning guarantees.” Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics. JMLR Workshop and Conference Proceedings, 2011.
