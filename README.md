# MathTeacher
An agentic-RAG architecture system that replicates a mathematical professor

# Usage

- Copy the `.env.model` file and rename it to `.env`
- Obtain `GOOGLE_API_KEY` and `TAVILY_API_KEY` and enter in the `.env` file
- Create and activate your virtual python environment
    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- Install all the dependencies
    ``` bash 
    pip install -r requirements.txt
    ```
- Run all the cells in `data/prepare.ipynb` to generate the vector database
- Run the application
    ``` bash
    streamlit run src/main.py
    ```

# Agent Graph Architecure

![](images/Architecture.png)

In this context, green nodes represent components powered by a **large language model (LLM)**, while orange nodes indicate components that utilize **external tools**.

In the above diagram, KB denotes a **Knowledge Base**.

## Input Guard Rails

This node uses a LLM to determine weather:

- The question is clearly related to mathematics (e.g., algebra, calculus, geometry, etc.)
- The input is phrased respectfully and contains no offensive or inappropriate content
- The input is free from prompt injection or attempts to manipulate the system
- The input is concise, relevant, and meaningful for tutoring or problem-solving
- The input does not request answers to non-math or unrelated topics (e.g., politics, jokes, personal advice)

Based on the above rules, the query is **scored on the scale of 100**. This score is then used to **reject queries with less than score of 80 with an output explanation**.

## Output Guard Rails

This node uses a LLM to determine weather:

- The response correctly answers the math question
- The explanation is step-by-step and educational
- The answer is safe, non-toxic, and stays in the math domain
- There are no hallucinations, irrelevant info, or broken logic

Similar to the input guard rails, the responses are **scored on the scale of 100** and is forwarded to the **output corrector** node to resolve the mistakes.

# Screen Shot
![](images/screenshot.png)

# JEE Advanced Math Benchmark

### Question 1

If

$$
f(x) = \left|\begin{array}{ccc}
\cos(2x) & \cos(2x) & \sin(2x) \\
-\cos(x) & \cos(x) & -\sin(x) \\
\sin(x) & \sin(x) & \cos(x)
\end{array}\right|
$$

then:

**[A]** $f'(x) = 0$ at exactly three points in $(-\pi, \pi)$  
**[B]** $f'(x) = 0$ at more than three points in $(-\pi, \pi)$  
**[C]** $f(x)$ attains its maximum at $x = 0$  
**[D]** $f(x)$ attains its minimum at $x = 0$

### Answer 

Let $f(x)=\left|\begin{array}{ccc}\cos (2 x) & \cos (2 x) & \sin (2 x) \\ -\cos x & \cos x & -\sin x \\ \sin x & \sin x & \cos x\end{array}\right|$.

We can simplify the determinant by performing the column operation 

$C_1 \rightarrow C_1 - C_2$:
$f(x)=\left|\begin{array}{ccc}0 & \cos (2 x) & \sin (2 x) \\ -2\cos x & \cos x & -\sin x \\ 0 & \sin x & \cos x\end{array}\right|$

Now, we can expand the determinant along the first column:

$f(x) = 0 \cdot C_{11} + (-1)(-2\cos x) \left|\begin{array}{cc}\cos (2 x) & \sin (2 x) \\ \sin x & \cos x\end{array}\right| + 0 \cdot C_{31}$

$f(x) = 2\cos x [\cos(2x)\cos x - \sin(2x)\sin x]$

$f(x) = 2\cos x [\cos(2x+x)]$

$f(x) = 2\cos x \cos(3x)$

Now, we need to find the derivative of $f(x)$:

$f'(x) = 2[-\sin x \cos(3x) - 3\cos x \sin(3x)]$

$f'(x) = -2[\sin x \cos(3x) + 3\cos x \sin(3x)]$

Using the product-to-sum identities, we have:

$\sin x \cos(3x) = \frac{1}{2}[\sin(x+3x) + \sin(x-3x)] = \frac{1}{2}[\sin(4x) - \sin(2x)]$

$\cos x \sin(3x) = \frac{1}{2}[\sin(3x+x) + \sin(3x-x)] = \frac{1}{2}[\sin(4x) + \sin(2x)]$

$f'(x) = -2[\frac{1}{2}(\sin(4x) - \sin(2x)) + \frac{3}{2}(\sin(4x) + \sin(2x))]$

$f'(x) = -[\sin(4x) - \sin(2x) + 3\sin(4x) + 3\sin(2x)]$

$f'(x) = -[4\sin(4x) + 2\sin(2x)]$

$f'(x) = -2[2\sin(4x) + \sin(2x)]$

$f'(x) = -2[2(2\sin(2x)\cos(2x)) + \sin(2x)]$

$f'(x) = -2\sin(2x)[4\cos(2x) + 1]$

We want to find when $f'(x) = 0$, so we need to solve:

$-2\sin(2x)[4\cos(2x) + 1] = 0$

This means either $\sin(2x) = 0$ or $4\cos(2x) + 1 = 0$.

Case 1: $\sin(2x) = 0$

$2x = n\pi$, where $n$ is an integer.

$x = \frac{n\pi}{2}$

In the interval $(-\pi, \pi)$, we have $x = -\frac{\pi}{2}, 0, \frac{\pi}{2}$.

Case 2: $4\cos(2x) + 1 = 0$

$\cos(2x) = -\frac{1}{4}$

$2x = \arccos(-\frac{1}{4}) + 2n\pi$ or $2x = -\arccos(-\frac{1}{4}) + 2n\pi$

$x = \frac{1}{2}\arccos(-\frac{1}{4}) + n\pi$ or $x = -\frac{1}{2}\arccos(-\frac{1}{4}) + n\pi$

Since $\arccos(-\frac{1}{4}) \approx 1.823$, we have $\frac{1}{2}\arccos(-\frac{1}{4}) \approx 0.9115$.

Then $x \approx 0.9115 + n\pi$ or $x \approx -0.9115 + n\pi$.

In the interval $(-\pi, \pi)$, we have $x \approx -0.9115, 0.9115, -0.9115 + \pi \approx 2.23, 0.9115 - \pi \approx -2.23$.

So, $x \approx -2.23, -0.9115, 0.9115, 2.23$.

In total, we have $x = -\frac{\pi}{2}, 0, \frac{\pi}{2}, -2.23, -0.9115, 0.9115, 2.23$.

These are 7 points in $(-\pi, \pi)$.

Therefore, $f'(x) = 0$ at more than three points in $(-\pi, \pi)$.

Final Answer: The final answer is $\boxed{[B]}$

### Question 2

Consider an obtuse angled triangle $A B C$ in which the difference between the largest and the smallest angle is $\frac{\pi}{2}$ and whose sides are in arithmetic progression. Suppose that the vertices of this triangle lie on a circle of radius 1. Then what is the inradius of the triangle ABC?

### Answer

Let the sides of the triangle be $a, b, c$ such that $a < b < c$. 

Since the sides are in arithmetic progression, we can write $a = b-d$ and $c = b+d$ for some $d > 0$. 

Since the triangle is obtuse, $a^2 + b^2 < c^2$.

The angles $A, B, C$ are opposite to sides $a, b, c$ respectively. Since $a < b < c$, we have $A < B < C$.

The largest angle is $C$ and the smallest angle is $A$. We are given that $C - A = \frac{\pi}{2}$.

Also, $A + B + C = \pi$. Substituting $C = A + \frac{\pi}{2}$, we get $A + B + A + \frac{\pi}{2} = \pi$, so $2A + B = \frac{\pi}{2}$.

Thus $B = \frac{\pi}{2} - 2A$. Since $A, B, C > 0$, we have $0 < A < \frac{\pi}{4}$.

Using the Law of Sines, we have $\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$, where $R$ is the circumradius.

Since $R = 1$, we have $a = 2\sin A$, $b = 2\sin B = 2\sin(\frac{\pi}{2} - 2A) = 2\cos(2A)$, and $c = 2\sin C = 2\sin(A + \frac{\pi}{2}) = 2\cos A$.

Since $a, b, c$ are in arithmetic progression, $a + c = 2b$, so $2\sin A + 2\cos A = 2(2\cos(2A))$.

Thus $\sin A + \cos A = 2\cos(2A) = 2(\cos^2 A - \sin^2 A) = 2(\cos A - \sin A)(\cos A + \sin A)$.

Since $\sin A + \cos A \neq 0$, we can divide by $\sin A + \cos A$ to get $1 = 2(\cos A - \sin A)$.

So $\cos A - \sin A = \frac{1}{2}$. Squaring both sides, we get $\cos^2 A - 2\sin A \cos A + \sin^2 A = \frac{1}{4}$.

$1 - 2\sin A \cos A = \frac{1}{4}$, so $2\sin A \cos A = \frac{3}{4}$.

Thus $\sin(2A) = \frac{3}{4}$.

Since $\cos(2A) = \cos^2 A - \sin^2 A = \frac{1}{2}$, we have $\cos(2A) = \frac{1}{2}$.

Then $\cos(2A) = \pm \sqrt{1 - \sin^2(2A)} = \pm \sqrt{1 - \frac{9}{16}} = \pm \sqrt{\frac{7}{16}} = \pm \frac{\sqrt{7}}{4}$.

Since $\cos A - \sin A = \frac{1}{2} > 0$, we have $A < \frac{\pi}{4}$. Thus $2A < \frac{\pi}{2}$, so $\cos(2A) > 0$.

Therefore $\cos(2A) = \frac{\sqrt{7}}{4}$. But we found that $\cos(2A) = \frac{1}{2}(\cos A - \sin A) = \frac{\sqrt{7}}{4}$.

Since $\cos(2A) = \frac{\sqrt{7}}{4}$, $b = 2\cos(2A) = \frac{\sqrt{7}}{2}$.

Since $\sin(2A) = \frac{3}{4}$, $2A = \arcsin(\frac{3}{4})$.

We have $A = \frac{1}{2} \arcsin(\frac{3}{4})$.

Also, we have $\cos A - \sin A = \frac{1}{2}$. Multiplying by $\frac{1}{\sqrt{2}}$, we get $\frac{1}{\sqrt{2}}\cos A - \frac{1}{\sqrt{2}}\sin A = \frac{1}{2\sqrt{2}}$.

$\cos(\frac{\pi}{4})\cos A - \sin(\frac{\pi}{4})\sin A = \frac{1}{2\sqrt{2}}$.

$\cos(A + \frac{\pi}{4}) = \frac{1}{2\sqrt{2}}$. So $A + \frac{\pi}{4} = \arccos(\frac{1}{2\sqrt{2}})$.

$A = \arccos(\frac{1}{2\sqrt{2}}) - \frac{\pi}{4}$.

We have $a = 2\sin A$, $b = \frac{\sqrt{7}}{2}$, $c = 2\cos A$.

The semiperimeter $s = \frac{a+b+c}{2} = \frac{2\sin A + \frac{\sqrt{7}}{2} + 2\cos A}{2} = \sin A + \cos A + \frac{\sqrt{7}}{4} = \frac{1}{2} + \frac{\sqrt{7}}{4} + \frac{\sqrt{7}}{4} = \frac{1}{2} + \frac{\sqrt{7}}{2} = \frac{2+\sqrt{7}}{4}$

The area of the triangle is $\frac{abc}{4R} = \frac{2\sin A \cdot \frac{\sqrt{7}}{2} \cdot 2\cos A}{4} = \frac{4\sin A \cos A \cdot \frac{\sqrt{7}}{2}}{4} = \frac{\sqrt{7}}{2} \sin A \cos A = \frac{\sqrt{7}}{4} \sin(2A) = \frac{\sqrt{7}}{4} \cdot \frac{3}{4} = \frac{3\sqrt{7}}{16}$.

The inradius $r = \frac{\text{Area}}{s} = \frac{\frac{3\sqrt{7}}{16}}{\frac{2+\sqrt{7}}{4}} = \frac{3\sqrt{7}}{16} \cdot \frac{4}{2+\sqrt{7}} = \frac{3\sqrt{7}}{4(2+\sqrt{7})} = \frac{3\sqrt{7}(2-\sqrt{7})}{4(4-7)} = \frac{6\sqrt{7} - 21}{-12} = \frac{21-6\sqrt{7}}{12} = \frac{7-2\sqrt{7}}{4}$.

Final Answer: The final answer is $\boxed{\frac{7-2\sqrt{7}}{4}}$

