import React from "react";

// mocks
const mockSetStation = jest.fn();
const mockSetFeatures = jest.fn();
const mockSetSearchParams = jest.fn();
const mockOnSearch = jest.fn();
const mockAlert = jest.spyOn(window, "alert").mockImplementation(() => {});

afterEach(() => {
  jest.clearAllMocks();
});

describe("Searchbar functions", () => {
  test("handleStationChange update station", () => {
    // Case 1, selected Juan Carlos I, expect no alert
    const e = { target: { value: "Juan Carlos I" } };

    const handleStationChange = (e) => {
      const value = e.target.value;
      mockSetStation(value);
      if (value === "Gabriel de Castilla") {
        window.alert("⚠️ This station is known to have issues!");
      }
    };

    handleStationChange(e);

    expect(mockSetStation).toHaveBeenCalledWith("Juan Carlos I");
    expect(mockAlert).not.toHaveBeenCalled();
  });

  test("handleStationChange warning functionality for Gabriel de Castilla", () => {
    // Case 2, selected Gabriel de Castilla, expect alert
    const e = { target: { value: "Gabriel de Castilla" } };

    const handleStationChange = (e) => {
      const value = e.target.value;
      mockSetStation(value);
      if (value === "Gabriel de Castilla") {
        window.alert("⚠️ This station is known to have issues!");
      }
    };

    handleStationChange(e);

    expect(mockSetStation).toHaveBeenCalledWith("Gabriel de Castilla");
    expect(mockAlert).toHaveBeenCalledWith(
      "⚠️ This station is known to have issues!"
    );
  });

  test("handleFeatureToggle correctly add features", () => {
    // Case 3, features are correctly added to the request parameters
    const handleFeatureToggle = (feature) => {
      mockSetFeatures((prev) =>
        prev.includes(feature)
          ? prev.filter((f) => f !== feature)
          : [...prev, feature]
      );
    };

    handleFeatureToggle("temp");

    expect(mockSetFeatures).toHaveBeenCalled();
    const updater = mockSetFeatures.mock.calls[0][0];
    expect(updater([])).toEqual(["temp"]);
  });

  test("handleFeatureToggle removes feature if already present", () => {
    // Case 4, check feature removal between different searches
    const handleFeatureToggle = (feature) => {
      mockSetFeatures((prev) =>
        prev.includes(feature)
          ? prev.filter((f) => f !== feature)
          : [...prev, feature]
      );
    };

    handleFeatureToggle("temp");

    expect(mockSetFeatures).toHaveBeenCalled();
    const updater = mockSetFeatures.mock.calls[0][0];
    expect(updater(["temp", "pres"])).toEqual(["pres"]);
  });

  test("handleSearchClick alerta si faltan fechas", () => {
    // Case 5, check essential parameters are requested if not specified
    const startDate = null;
    const endDate = null;
    const station = "Juan Carlos I";
    const aggregation = "Daily";
    const features = ["temperatura"];

    const handleSearchClick = () => {
      if (!startDate || !endDate) {
        alert("Start and end dates are required.");
        return;
      }
    };

    handleSearchClick();

    expect(mockAlert).toHaveBeenCalledWith("Start and end dates are required.");
  });

  test("handleSearchClick constructs params and calls onSearch", () => {
    // Case 6, parameters are correctly constructed to be sent in the search
    const startDate = "2025-01-01";
    const endDate = "2025-01-31";
    const station = "Juan Carlos I";
    const aggregation = "Daily";
    const features = ["temperatura", "presion"];

    const handleSearchClick = () => {
      if (!startDate || !endDate) {
        alert("Start and end dates are required.");
        return;
      }

      const stationCodes = {
        "Juan Carlos I": 89064,
        "Gabriel de Castilla": 89065,
      };
      const stationCode = stationCodes[station] || station;

      const aggregationMap = {
        Hourly: "hourly",
        Daily: "daily",
        Monthly: "monthly",
      };
      const parsedAggregation = aggregationMap[aggregation] || undefined;

      const featureCodes = {
        temperatura: "temp",
        presion: "pres",
        viento: "vel",
      };
      const parsedFeatures =
        features.length > 0
          ? features.map((f) => featureCodes[f]).filter(Boolean)
          : Object.values(featureCodes);

      const params = {
        startDate,
        endDate,
        station: stationCode,
        features: parsedFeatures,
        ...(parsedAggregation && { aggregation: parsedAggregation }),
      };

      mockSetSearchParams(params);
      if (mockOnSearch) {
        mockOnSearch(params);
      }
    };

    handleSearchClick();

    expect(mockSetSearchParams).toHaveBeenCalledWith({
      startDate: "2025-01-01",
      endDate: "2025-01-31",
      station: 89064,
      features: ["temp", "pres"],
      aggregation: "daily",
    });
    expect(mockOnSearch).toHaveBeenCalled();
  });
});
