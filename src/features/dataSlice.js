import { createSlice, createAsyncThunk, current } from "@reduxjs/toolkit";
import { load } from "js-yaml";
import { isEmptyValue } from "../common/utils";

export const dataInitialize = createAsyncThunk(
  "data/dataInitialize",
  async () => {
    const result = await import.meta.glob("../posts/*.md", {
      eager: true,
      as: "raw",
    });

    return result;
  }
);

const initialState = {
  data: [],
  list: [],
  detail: {},
  category: {},
};

export const dataSlice = createSlice({
  name: "data",
  initialState,
  reducers: {
    getList: (state, action) => {
      const id = action?.payload?.replace(" ", "-")?.toLowerCase();
      const c = current(state.category);
      if (isEmptyValue(id)) {
        let list = [];
        Object.entries(c).forEach((item) => {
          list = [...list, ...item[1]];
        });
        state.list = list;
      } else {
        state.list = Object.entries(c).find(
          (e) => e[0].replace(" ", "-")?.toLowerCase() === id
        )[1];
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(dataInitialize.fulfilled, (state, action) => {
      const rawData = action.payload;

      const contents = Object.entries(rawData).map((file) => {
        return file[1];
      });

      const frontMatterRegex = /^---\n([\s\S]*?)\n---/;
      const list = {};
      contents.forEach((item) => {
        const match = item.match(frontMatterRegex);
        const header = load(match[1]);
        const id = header.category;
        const content = {
          categoryId: id?.replace(" ", "-")?.toLowerCase(),
          header: header,
          content: item.split(match[0])[1],
        };

        if (list?.[id]?.length > 0) {
          list[id] = [...list[id], content];
        } else {
          list[id] = [content];
        }
      });

      state.data = contents;
      state.category = list;
    });
  },
});

export const { getList } = dataSlice.actions;
export default dataSlice.reducer;
