import { useEffect, useState } from "react";
import { useTheme } from "@mui/material";

import Markdown from "react-markdown";
import { load } from "js-yaml";

import {
  materialDark,
  materialLight,
} from "react-syntax-highlighter/dist/cjs/styles/prism";
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
import item from "../posts/2023-11-18-vite.md";
// import item from "../posts/README.md";

const Content = () => {
  const theme = useTheme();

  const [header, setHeader] = useState({});
  const [content, setContent] = useState(null);

  const handleContent = (text) => {
    const frontMatterRegex = /^---\n([\s\S]*?)\n---/;
    const match = text.match(frontMatterRegex);
    setContent(text.split(match[0])[1]);
    setHeader(load(match[1]));
  };

  useEffect(() => {
    fetch(item)
      .then((res) => res.text())
      .then(handleContent);
  }, []);

  return (
    <Markdown
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || "");
          return !inline && match ? (
            <SyntaxHighlighter
              language={match[1]}
              PreTag="div"
              {...props}
              style={
                theme.palette.mode === "dark" ? materialDark : materialLight
              }
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
  );
};

export default Content;
