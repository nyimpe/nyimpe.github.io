import { Container, useTheme } from "@mui/material";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import Markdown from "react-markdown";
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

const DetailPage = () => {
  const theme = useTheme();
  const param = useParams();
  const dispatch = useDispatch();
  const [detail, setDetail] = useState({});
  const { category } = useSelector((state) => state.data);

  useEffect(() => {
    const { id } = param;
    Object.entries(category).forEach((item) => {
      const data = item[1].find((e) => e.pageId === id);
      if (data) {
        setDetail(data);
        return;
      }
    });
  }, [dispatch, category, param]);

  return (
    <Container>
      <Markdown
        components={{
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || "");
            return !inline && match ? (
              <SyntaxHighlighter
                language={match[1]}
                PreTag="div"
                {...props}
                codeTagProps={{
                  style: {
                    fontFamily: "IBMPlexSansKR",
                    wordSpacing: "1px",
                    letterSpacing: "1px",
                  },
                }}
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
        {detail?.content}
      </Markdown>
    </Container>
  );
};

export default DetailPage;
