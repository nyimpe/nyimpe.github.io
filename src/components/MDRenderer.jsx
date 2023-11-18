import { useEffect, useState } from "react";
import { Container } from "@mui/material";

import Markdown from "react-markdown";
import { load } from "js-yaml";

import { materialDark } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
import typescript from "react-syntax-highlighter/dist/cjs/languages/prism/typescript";
import bash from "react-syntax-highlighter/dist/cjs/languages/prism/bash";
import markdown from "react-syntax-highlighter/dist/cjs/languages/prism/markdown";
import json from "react-syntax-highlighter/dist/cjs/languages/prism/json";

SyntaxHighlighter.registerLanguage("typescript", typescript);
SyntaxHighlighter.registerLanguage("bash", bash);
SyntaxHighlighter.registerLanguage("markdown", markdown);
SyntaxHighlighter.registerLanguage("json", json);

// import item from "../posts/2023-11-12-First.md";
import item from "../posts/README.md";

const MDRenderer = () => {
  const [content, setContent] = useState("");

  const getPostList = () => {
    const mdFiles = import.meta.glob("../posts/*.md");

    // console.log(mdFiles);
    Object.keys(mdFiles).map((filePath) => {
      //   console.log(filePath);
    });
  };

  useEffect(() => {
    const frontMatterRegex = /^---\n([\s\S]*?)\n---/;
    const match = content.match(frontMatterRegex);
    if (match && match[1]) {
      console.log("match->", match[1]);
      // console.log("match->", load(match[1]));
    }
    getPostList();
  }, [content]);

  useEffect(() => {
    fetch(item)
      .then((res) => res.text())
      .then((text) => setContent(text));
  }, []);

  return (
    <Container fixed>
      <Markdown
        components={{
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || "");
            return !inline && match ? (
              <SyntaxHighlighter
                language={match[1]}
                PreTag="div"
                {...props}
                style={materialDark}
              >
                {String(children).replace(/\n$/, "")}
              </SyntaxHighlighter>
            ) : (
              <code {...props}>{children}</code>
            );
          },
        }}
      >
        {content}
      </Markdown>
    </Container>
  );
};

export default MDRenderer;
