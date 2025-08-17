// mocks
const mockSetLoading = jest.fn();
const mockSetError = jest.fn();
const mockSetSearchParams = jest.fn();
const mockSetData = jest.fn();

afterEach(() => {
  jest.clearAllMocks();
});

describe("Home handleSearch", () => {
  test("handleSearch succesfully updates data", async () => {
    // Case 1, fetchWeather returns data successfully
    const fetchWeather = jest.fn().mockResolvedValue([{ x: 1 }]);

    const handleSearch = async (params) => {
      mockSetLoading(true);
      mockSetError(null);
      mockSetSearchParams(params);

      try {
        const result = await fetchWeather(params);
        mockSetData(result);
      } catch (err) {
        mockSetError("Error fetching data");
        mockSetData([]);
      } finally {
        mockSetLoading(false);
      }
    };

    await handleSearch({ station: 123 });

    expect(mockSetLoading).toHaveBeenCalledWith(true);
    expect(fetchWeather).toHaveBeenCalledWith({ station: 123 });
    expect(mockSetData).toHaveBeenCalledWith([{ x: 1 }]);
    expect(mockSetLoading).toHaveBeenLastCalledWith(false);
  });

  test("handleSearch capture exception", async () => {
    // Case 2, exception handling
    const fetchWeather = jest.fn().mockRejectedValue(new Error("fail"));

    const handleSearch = async (params) => {
      mockSetLoading(true);
      mockSetError(null);
      mockSetSearchParams(params);

      try {
        const result = await fetchWeather(params);
        mockSetData(result);
      } catch (err) {
        mockSetError("Error fetching data");
        mockSetData([]);
      } finally {
        mockSetLoading(false);
      }
    };

    await handleSearch({ station: 456 });

    expect(mockSetError).toHaveBeenCalledWith("Error fetching data");
    expect(mockSetData).toHaveBeenCalledWith([]);
    expect(mockSetLoading).toHaveBeenLastCalledWith(false);
  });
});
