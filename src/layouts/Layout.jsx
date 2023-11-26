import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { Outlet } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Box, Container, CssBaseline, Toolbar } from "@mui/material";

import SideBar from "../components/SideBar";
import Breadcrum from "../components/Breadcrum";
import Header from "../components/Header";
import { dataInitialize } from "../features/dataSlice";

const Layout = () => {
  const dispatch = useDispatch();
  const [mode, setMode] = useState("dark");
  const [drawerToggle, setDrawerToggle] = useState(false);
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

  useEffect(() => {
    dispatch(dataInitialize());
  }, [dispatch]);

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Header handleMenuIcon={() => setDrawerToggle(true)} />
        <SideBar
          mode={mode}
          modeToggle={modelToggle}
          drawerToggle={drawerToggle}
          setDrawerToggle={setDrawerToggle}
        />
        <Container>
          <Toolbar
            sx={{
              display: { lg: "none", md: "none", sm: "block", xs: "block" },
            }}
          />
          <Breadcrum />
          <Outlet />
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;
