---
title: "Posterior Probability"
date: 2026-11-11
categories: [Math]
tags: [concept]
math: true
image:
    path: /assets/img/post_proba2.png
    alt: In order to know, we must assume.— Prof. Bharath B N, (IIT Dharward)
---
## Information and Probability
I present you a fair coin, that turns up heads or tails fifty-fifty. I toss it and hold it between my palms and sneak a peak for myself. I ask,
>What is the probability that the coin has turned up heads when I open my palms?

Now, I know the outcome that it is indeed tails. However, you don't see the coin. I would answer zero. Either you could say that the question is meaningless since the coin has already turned up as something, it is a matter of knowing the information from the past. Or you could answer based on only what you know - that the coin is fair - and you say half.
>In this sense, under incomplete information, probability can be used to have some opinion about what may happen next.

## Pain of Prejudice
This time, you take the coin from me and toss it two more times and landing on tails. What is the chance it lands on heads the next try? You say: "Half! because the tosses are independent!". Good!

_I may say the coin is fair, but it need not be. Why would you assume I am telling the truth?_ If you saw the same episode of me tossing thrice and getting tails all three times, would you assume the coin is fair? How would you estimate the chance the same coin lands on heads the next try?

>If you don't know the bias of the coin, does your estimate change as you see outcomes of more trials? So far, the coin has been tossed thrice and it has landed only on tails.


<div style="display:none">
$$\newcommand{\p}{\mathcal{P}}$$
$$\newcommand{\coloneqq}{:=}$$
$$\newcommand{\I}{\mathbb{1}}$$
$$\newcommand{\E}{\mathbb{E}}$$
</div>


## Assume so we may know
The coin has some bias $\theta$, however you do not know this. As far you know, you do not have any reason to believe I picked $\theta \geq 0.75$ or $\theta \leq 0.25$. No one value of $\theta$ is more likely than the other from your perspective. Well to be perfectly honest, I would imagine it is hard to make a coin with high bias, but let us not overthink. Regardless, the value has been picked, it is possible that even I know it. _In reality it may not have come from a distribution at all. But then under incomplete information you assume, so you can afford an opinion._

<blockquote class="prompt-tip">
<strong>Assumption:</strong> The bias of the coin $\theta$ is sampled from a uniform distribution.<br>
$$
\theta \sim \text{Uniform}[0,1]
$$
However, $\theta$ is unknown to you. As you see more data, your belief about $\theta$ improves.
</blockquote>

## Formalization
We follow the textbook[^lattimore2020] referenced below, but adapt it to our example for continuity. In our setting, the coin I brought is tossed three times. Your challenge is to figure the bias $\theta$ of the coin.


### Prior probability
Let $(\Theta, \mathcal{G}, Q)$ be a probability space. Here, $\Theta = [0,1]$ the sample space, set of all possible outcomes for the $\theta$ sample. $\mathcal{G} = \mathcal{B}([0, 1])$, the smallest $\sigma$-algebra containing all open intervals in $[0,1]$. ($\mathcal{G}$ is the set of all non-weird subsets of $[0,1]$. There are issues with writing off all subsets.) The function $Q$ represents the probability measure:

$$
Q: \mathcal{G} \rightarrow \mathcal{R}\quad Q(A) \coloneqq \Pr(\theta \in A)
$$

For here, we have, $Q([0,1]) = 1$. $Q(\phi)=0$ and $Q([0.25, 0.7]) = 0.45$. Thus, in this setting, we have assumed a uniform prior $Q$ on the coin's bias $\theta$. Formally, the prior $Q$ is a probability measure on the space $(\Theta, \mathcal{G})$


### Conditional
Let us denote the three outcomes by $X_1, X_2, X_3$. Before we talk about the bias, the list of outcomes of 3 coin tosses remain the same. Namely,

$$
\begin{align*}
S&\coloneqq\text{\{HHH, HHT, HTH, THH, TTH, THT, HTT, TTT\}}.\\
\mathcal{H} &\coloneqq 2^S
\end{align*}
$$

Set of all events $\mathcal{S}$ is just the powerset with $2^8=256$ subsets. So $(S, \mathcal{H})$ is a measurable space.

Now comes the bias $\theta$. If we knew $\theta=t$, recalling that the tosses are independent as you answered before, you answer the straightforward question

$$
P_\theta(\{\text{HHT}\}) = \Pr(X_1=H, X_2=H, X_3=T, \theta=\theta) = \theta ^2 \times (1-\theta).
$$

If you add many items in the set, you would sum $P_\theta$ over each item.

$$
P_\theta(\{\text{HHT, TTH, HTH}\}) = 2\theta ^2(1-\theta) + (1-\theta)^2\theta.
$$

For a given $\theta$, we have a definitive probability space $(S, \mathcal{S}, P_\theta)$. The possibilities are the same, but the probabilities differ due to $\theta$. This $P = (P_\theta, \,\,\theta \in \Theta)$ is called a model, and also a probability kernel from $(\Theta, \mathcal{G})$ to $(S, \mathcal{H})$.

### Joint probability
The prior and the model combine:
* $\Omega = \Theta \times S$ represents the combined sample-space, a point representing $(\theta, X_1, X_2, X_3)$ jointly $\omega = (0.314, HHT)$ is a member of $\Omega$.
* $\mathcal{F} = \mathcal{G} \otimes \mathcal{H}$ represents the joint $\sigma$-algebra. Events involving both $\theta$ and $X_1, X_2, X_3$ are in this set. If $A = [0.25, 0.7] \times \\{HHT, HHH\\}$, then this event $A \in \mathcal{F}$.
* $\mathbb{P} = Q \otimes P$ is the joint probability measure that answers questions like $\mathbb{P}(A) = \text{some value}$. For any set $B \in \mathcal{G}$, the prior probability can be written in terms of the joint measure: $Q(B) = \mathbb{P}(B \times S)$.




[^lattimore2020]: Lattimore, T., & Szepesvári, C. (2020). *Bandit Algorithms*. Cambridge University Press. https://doi.org/10.1017/9781108571401
