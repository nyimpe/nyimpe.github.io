import { useNavigate } from "react-router-dom";
import {
  Avatar,
  Box,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Typography,
} from "@mui/material";

import HomeIcon from "@mui/icons-material/Home";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import DataArrayIcon from "@mui/icons-material/DataArray";
import DataObjectIcon from "@mui/icons-material/DataObject";
import CodeIcon from "@mui/icons-material/Code";
import BuildIcon from "@mui/icons-material/Build";
// import NewspaperIcon from "@mui/icons-material/Newspaper";
// import ApiIcon from "@mui/icons-material/Api";
// import BoltIcon from "@mui/icons-material/Bolt";
// import JavascriptIcon from "@mui/icons-material/Javascript";
import img from "../assets/images/profile.png";
import { useSelector } from "react-redux";

const ICONS = [
  <DataArrayIcon key={0} />,
  <DataObjectIcon key={1} />,
  <CodeIcon key={2} />,
  <BuildIcon key={3} />,
];

const SideBar = ({ mode, modeToggle, drawerToggle, setDrawerToggle }) => {
  const { category } = useSelector((state) => state.data);
  const navigate = useNavigate();

  const drawer = () => {
    return (
      <>
        <Box sx={{ textAlign: "center", mt: 2, mb: 5 }}>
          <Avatar
            src={img}
            sx={{ width: 150, height: 150, margin: "0px auto" }}
          />
          <Typography
            variant="h5"
            sx={{ mt: 3, fontFamily: "cursive, Poppins, sans-serif" }}
          >
            Hello Sushi
          </Typography>
          <Typography
            mt={1}
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 12,
            }}
            gap={1}
          ></Typography>
        </Box>
        <Box sx={{ height: "90%" }}>
          <List>
            <ListItem>
              <ListItemButton onClick={() => navigate("/")}>
                <ListItemIcon>
                  <HomeIcon />
                </ListItemIcon>
                HOME
              </ListItemButton>
            </ListItem>
            {Object.keys(category).length > 0 ? (
              <>
                {Object.keys(category).map((e, i) => {
                  return (
                    <ListItem key={e}>
                      <ListItemButton
                        onClick={() =>
                          navigate(`/${category[e][0].categoryId}`)
                        }
                      >
                        <ListItemIcon>{ICONS[i]}</ListItemIcon>
                        <Typography>{e}</Typography>
                      </ListItemButton>
                    </ListItem>
                  );
                })}
              </>
            ) : null}
          </List>
        </Box>
        <Box sx={{ textAlign: "center", mb: 3 }}>
          <IconButton onClick={modeToggle} color="inherit">
            {mode === "dark" ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>
        </Box>
      </>
    );
  };

  return (
    <>
      <Drawer
        sx={{
          width: 250,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: 250,
            boxSizing: "border-box",
            justifyContent: "space-between",
          },
          display: { lg: "block", md: "block", sm: "none", xs: "none" },
        }}
        variant="permanent"
        ModalProps={{ keepMounted: true }}
        anchor="left"
        open={drawerToggle}
        onClose={() => setDrawerToggle(false)}
      >
        {drawer()}
      </Drawer>
      <Drawer
        variant="temporary"
        open={drawerToggle}
        onClose={() => setDrawerToggle(false)}
        ModalProps={{ keepMounted: true }}
        sx={{
          "& .MuiDrawer-paper": {
            width: 250,
            boxSizing: "border-box",
            justifyContent: "space-between",
          },
          display: { lg: "none", md: "none", sm: "block", xs: "block" },
        }}
      >
        {drawer()}
      </Drawer>
    </>
  );
};

export default SideBar;
