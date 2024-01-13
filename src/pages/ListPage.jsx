import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { nanoid } from "@reduxjs/toolkit";
import dayjs from "dayjs";
import { Box, Card, CardContent, Typography } from "@mui/material";
import JavascriptIcon from "@mui/icons-material/Javascript";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";

import { getList } from "../features/dataSlice";
import { isEmptyValue } from "../common/utils";

const ListPage = () => {
  const { pathname } = useLocation();
  const param = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { category, list } = useSelector((state) => state.data);
  const [contents, setContents] = useState([]);

  const handleDetailPage = (id) => {
    const url = `${pathname === "/" ? "/home" : pathname}/${id}`;
    navigate(url);
  };

  useEffect(() => {
    if (isEmptyValue(category)) {
      return;
    }
    dispatch(getList(param.category));
  }, [category, param, dispatch]);

  useEffect(() => {
    if (list.length < 1) {
      return;
    }

    const sortedList = [...list];
    sortedList.sort((a, b) => {
      return b.header.date - a.header.date;
    });

    setContents(sortedList);
  }, [list]);

  return (
    <Box sx={{ my: 3 }}>
      {!isEmptyValue(contents)
        ? contents.map((item) => {
            return (
              <Card key={nanoid()} sx={{ my: 2 }} variant="outlined">
                <CardContent>
                  <Typography
                    fontSize={18}
                    fontWeight={"bold"}
                    gutterBottom
                    sx={{ cursor: "pointer" }}
                    onClick={() => handleDetailPage(item.header.id)}
                  >
                    {item.header.title}
                  </Typography>
                  <Typography
                    sx={{
                      my: 1,
                      maxHeight: 50,
                      overflow: "hidden",
                      wordBreak: "break-word",
                      cursor: "pointer",
                    }}
                    color="text.secondary"
                    onClick={() => handleDetailPage(item.header.id)}
                  >
                    {item.content}
                  </Typography>
                  <Box
                    sx={{
                      display: "flex",
                      gap: 1,
                      mt: 2,
                      alignItems: "center",
                    }}
                  >
                    <CalendarMonthOutlinedIcon />
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ mr: 5 }}
                    >
                      {dayjs(item.header.date).format("YYYY.MM.DD.")}
                    </Typography>

                    <JavascriptIcon />
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      onClick={() => navigate(`/${item.categoryId}`)}
                    >
                      {item.header.category}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            );
          })
        : null}
    </Box>
  );
};

export default ListPage;
