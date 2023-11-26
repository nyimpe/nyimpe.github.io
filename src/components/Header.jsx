import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import useScrollTrigger from "@mui/material/useScrollTrigger";
import Slide from "@mui/material/Slide";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";
import IconButton from "@mui/material/IconButton";
import { Box } from "@mui/material";

const Header = ({ handleMenuIcon }) => {
  const HideOnScroll = ({ children }) => {
    const trigger = useScrollTrigger();

    return (
      <Slide
        appear={false}
        direction="down"
        in={!trigger}
        sx={{ display: { lg: "none", md: "none", sm: "block", xs: "block" } }}
      >
        {children}
      </Slide>
    );
  };

  return (
    <>
      <HideOnScroll>
        <AppBar>
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
              onClick={handleMenuIcon}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              variant="h6"
              component="div"
              sx={{ fontFamily: "cursive, Poppins, sans-serif" }}
            >
              Hello Sushi
            </Typography>
            <IconButton edge="end" color="inherit">
              <SearchIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
      </HideOnScroll>
    </>
  );
};

export default Header;
