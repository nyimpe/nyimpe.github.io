import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { load } from "js-yaml";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Box, Container, CssBaseline } from "@mui/material";

import SideBar from "../components/SideBar";
import Breadcrum from "../components/Breadcrum";

const Layout = () => {
  const [mode, setMode] = useState("dark");
  const [dataList, setDataList] = useState({});
  const darkTheme = createTheme({
    palette: {
      mode: mode,
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          html: {
            fontFamily: "Poppins, sans-serif",
          },
          body: {
            fontFamily: "Poppins, sans-serif",
          },
        },
      },
    },
  });

  const modelToggle = () => {
    setMode(mode === "dark" ? "light" : "dark");
  };

  const handleData = (data) => {
    const frontMatterRegex = /^---\n([\s\S]*?)\n---/;
    const list = {};
    data.forEach((item) => {
      const match = item.match(frontMatterRegex);
      const header = load(match[1]);
      const content = { header: header, content: item.split(match[0])[1] };

      if (list?.[header.categories[0]]?.length > 0) {
        list[header.categories[0]] = [...list[header.categories[0]], content];
      } else {
        list[header.categories[0]] = [content];
      }
    });
    setDataList(list);
  };

  // useEffect(() => {
  //   console.log("dataList->", dataList);
  // }, [dataList]);

  useEffect(() => {
    // const env = import.meta.env;
    // Object.entries(env).forEach((item) => {
    //   sessionStorage.setItem(item[0], item[1]);
    // });
    const mdFiles = import.meta.glob("/nyimpe.github.io/posts/*.md", {
      eager: true,
    });

    const fetchData = async () => {
      const contents = await Promise.all(
        Object.entries(mdFiles).map(async (file) => {
          const content = await import(file[0]).then(
            (module) => module.default
          );
          const data = await fetch(content).then((res) => res.text());
          return data;
        })
      );
      handleData(contents);
    };

    fetchData();
  }, []);

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <SideBar mode={mode} modeToggle={modelToggle} dataList={dataList} />
        <Container fixed>
          <Breadcrum />
          <Outlet />
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;
