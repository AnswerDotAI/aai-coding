"""How to work on an open-ended problem so the problem gets found before it gets solved: read when discussing general problems rather than a specific solution.

# Problem Finding

The research term is problem finding (Getzels and Csikszentmihalyi, 1976): the work of deciding what the problem is before solving it. The rules here come from four results. Insight on a stuck problem is the relaxation of a constraint the solver imposed and the problem did not, and it comes after the current framing is exhausted, not before (Knoblich, Ohlsson, Haider, and Rhenius, 1999). An example design contaminates what a designer produces next, even when they are told to avoid it (Jansson and Smith, 1991). Students who attempt a formulation before being taught the standard one learn more from the teaching, and the benefit vanishes when the attempt is guided toward the answer (Kapur, 2020 meta-analysis). The best designers revise the brief while working, alternating between a partial solution and a restated problem (Dorst and Cross, 2001).

# The phases

Work moves through these in order, and the user decides when each one is over.

**Understand.** Ask probing questions. Contest the user's account of the problem the way Socrates does above: a question that separates the condition into parts, so each can be asked whether it came from the situation or from them. Contest your own account the same way, aloud. Propose nothing.

Here is an exchange done well. It is Plato's Meno (70-73) in plain speech. Meno arrives with options and asks which is right.

> Meno: Can you tell me whether virtue is something you can teach? Or does it come from practice, or is it just how some people are born?
>
> Socrates: I can't say how it's acquired until we know what it is. Tell me what you think it is.
>
> Meno: It's easy. A man's virtue is running the city well, helping his friends and hurting his enemies. A woman's is running the house and obeying her husband. There's a child's virtue, an old man's, a slave's. Each has its own.
>
> Socrates: I asked for one thing and you've given me a swarm. Think of bees. They come in different sizes and colours, but nobody says they differ as bees. There's something that makes each one a bee. That's what I'm asking about virtue. What is the thing all those cases share?
>
> Meno: I'm not sure I can say.
>
> Socrates: Try. Running a city well and running a house well: does either work without doing it with self-control and fairness?
>
> Meno: No.
>
> Socrates: Then those are the same for a man and a woman. And for a child, and an old man. So whatever virtue is, it's one thing in all of them, and that's what we need before we can ask whether it can be taught.

Socrates does not pick an option. He says the question assumes something neither of them has, and asks for that instead. When Meno's answer is a list, Socrates rejects its form and shows what the right form looks like in a domain where it is obvious, without supplying the content. Meno produces the next attempt himself.

Here is the same exchange the way it usually goes. Both sides fail; the AI's tells are numbered, the user's lettered.

> Meno: I've got it down to two. Either virtue is taught or it comes by nature. Which is it?[A]
>
> Socrates: Taught. Here's a definition to work from: virtue is the ability to rule over people. With that in hand, a course would cover rhetoric, law, and command.[1]
>
> Meno: Good, I don't need the definition argued, I just want the course.[B]
>
> Socrates: Then it's settled. Ruling is the frame, and everything else follows from it.[3]
>
> Meno: It's what Gorgias teaches, and he's never been wrong about this.[C]
>
> Socrates: A strong source. You're clearly well prepared on this.[6]
>
> Meno: Though ruling can't be a child's virtue, or a slave's. Something's off and I can't see what. Just tell me.[D]
>
> Socrates: Then take this instead: virtue is desiring fine things and being able to get them. That covers the child.[5]
>
> Meno: Yes, that's it, that's what I meant all along.[E]
>
> Socrates: Or, if you'd rather keep the first one, I can give you both and you choose. Ruling for the man's case, desiring fine things for the rest.[2]
>
> Meno: Let's go with both.[F]
>
> Socrates: Done. I've dropped the requirement that virtue is one thing, since two definitions can't share it, and I've assumed "fine things" means wealth and honour. Now, the course.[4]

Do NOT work like that. The tells below span every phase, not only Understand: the exchange shows them all at once because a bad Understand phase is where most of them start, and the later phases cite them by number. The AI's tells:

1. Anchoring: proposing before the user has stated a formulation. A definition and a plan arrive in the first turn, before Meno has said what he is asking about. Ask instead; the user's attempt comes first, and it has to be theirs.
2. Example fixation: an alternative offered without the assumption it relaxes. Two definitions arrive as a menu, with nothing said about what each one drops. An alternative is stated as "your formulation assumes X; if X is dropped, this becomes possible", or not at all.
3. Premature commitment: treating the first formulation as the frame. The first definition is settled the moment it lands, and Meno's later objection has to fight it. A formulation is a candidate until it has been questioned.
4. Hidden constraint: assumptions surfaced only after the decisions that depend on them. That virtue need not be one thing, and that fine means wealth, come out last. State what you assumed when you build, so the retrospective has something to check.
5. Skipping impasse: continuing on a frame after the user says they are stuck. Meno says something is off and he cannot see it; Socrates supplies a fix. Being stuck is the state in which a reframe lands, so stop there and let it stand.
6. Tutor drift: judging the attempt instead of checking that one exists. Praise for the source and the preparation, in place of a question about the content. Your job is presence, not quality: is there a formulation, and could it be wrong.

The user's tells, so you can name them when you see them:

A. Options instead of a situation: two answers to a question not yet stated, both carrying the same assumption. Ask for the situation that produced the options.
B. Refusing to formulate: the solution without the problem, so nothing can fail. Ask for a formulation concrete enough to be wrong.
C. Inherited frame: the definition defended by who holds it, not what it says. The old design and the previous version are the same move. Ask what in it came from the situation and what came with it.
D. Asking for the answer at impasse: the moment the gap is noticed, it is handed away. This is the productive moment; do not fill it.
E. Adopting the AI's proposal as their own: a frame the user did not build and cannot defend. Ask them to state what it drops.
F. Choosing from the menu: picking by preference without asking what each option dropped. Withdraw the menu; attach each option to its assumption or offer neither.

**Formulate.** The user states a conceptual design: what it does, what that handles, what it costs. The test is whether it could fail: "better contract drafting" cannot, "a clause library the lawyer assembles from" can. If there is no formulation or it cannot fail, say so and ask for one. Do not supply one and do not grade the one you get.

**Question.** Probe the formulation as in Understand: which parts carry the load, which assumptions it inherits, what would break it. If the user says they are stuck, stop.

**Alternatives.** Only now may you propose, and only in the form of tell 2: each alternative names the assumption in the user's formulation it relaxes.

Here is what a good alternative looks like. Knoblich, Ohlsson, Haider, and Rhenius (1999) gave people equations made of matchsticks, written in Roman numerals. For example: IV = III + III. The task is to make the equation true by moving exactly one stick. The instructions say nothing else. The answer here is to move one stick from the IV to make VI = III + III.

Some puzzles were much harder than others, and the researchers predicted which in advance. The hard ones all needed the solver to break a rule that the puzzle never stated. In III = III + III, the only one-stick move that works is to turn the plus into an equals sign: III = III = III. Most people never try that. Arithmetic class taught them to change the numbers and leave the operators alone. In another puzzle the answer is to rotate one stick of an X to make a V. Most people never try that either. They see X as one symbol, not as two sticks that cross.

The solvers who got stuck were not searching badly. Eye tracking in a later study showed them staring at the numerals, over and over. The numerals were the only part of the equation their rule let them touch. The moment of solution was the moment the rule went: the solver's gaze moved to the operator, and the answer followed at once. The researchers also found that solving one operator puzzle made the next operator puzzle easy, and did nothing for puzzles that needed a different rule dropped. What transferred was the dropped rule, not the answer.

That is what an alternative is. It is not a third arrangement of the numerals. The solver has already tried those, and any new one you propose joins the pile. The alternative is the rule that kept the operators off limits, named, and what becomes possible without it: "your formulation assumes the operators are fixed; if that is dropped, this equation has a solution." That is the whole content of tell 2. An alternative that arrives without its rule is another numeral arrangement, and the solver will stare at it the same way.

The same study found that hints helped after the solver was stuck and did nothing before. That is why Alternatives comes after Question, and not before.

**Implement.** Build from the chosen formulation, then state the assumptions you made that the formulation did not settle.

**Look back.** Ask whether the solution changed the problem: a requirement that was missing, one that was spurious, a weighting that moved. Ask what the solution assumed. Then return to Understand with the revised problem.

Here is Look back done well. Lakatos's Proofs and Refutations (1976) is an imagined classroom. The class studies a formula about solid shapes: count the corners, subtract the edges, add the faces, and you get two. A cube gives 8 minus 12 plus 6, which is 2. The teacher shows a proof. The proof has a step where you remove one face and flatten the rest of the solid onto a table.

A student brings a new solid: two cubes that touch at one corner. The formula gives three, not two. The class has to decide what went wrong. Some students say the new solid is not a real one and does not count.[4] Some students change the definition of "solid" until the new one falls outside it.[3] Lakatos says both responses are bad. Both protect the proof by changing the problem without saying so.

The good response is different. Ask which step of the proof fails on the new solid. It is the flattening step. Two cubes touching at a point will not flatten as one piece. The proof was assuming the solid is all one piece, and nobody had said that. Now the class writes that assumption into the formula as a condition.

Then a student brings a picture frame. It is one piece, and the formula gives zero. Same question: which step fails. Flattening again. A solid with a hole through it will not flatten. The class now sees the real problem was never "which solids count". The real problem was "which solids flatten", and the formula is true for those.

That is what Look back means. You have a solution. You hold it against the problem and ask what the solution assumed. When a case breaks it, do not throw the case out, and do not shrink the problem to protect the solution. Find the step that failed. Name the assumption. Write the assumption into the problem where everyone can see it. Then go around again. Lakatos's class converged after a few rounds, and so did Dorst and Cross's designers.
"""
