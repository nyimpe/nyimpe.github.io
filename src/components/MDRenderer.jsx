import { useEffect, useState } from "react";
import { load } from "js-yaml";

import Markdown from "react-markdown";
import item from "../posts/2023-11-12-First.md";

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
      console.log("match->", load(match[1]));
    }
    getPostList();
  }, [content]);

  useEffect(() => {
    fetch(item)
      .then((res) => res.text())
      .then((text) => setContent(text));
  }, []);

  return <Markdown>{content}</Markdown>;
};

export default MDRenderer;
