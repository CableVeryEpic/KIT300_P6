import OpenAI from "openai";

const client = new OpenAI();

const completion = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
        {
            role: "user",
            content: "translate the chinese name Quan Bai into IPA",
        },
    ],
});

console.log(completion.choices[0].message.content);