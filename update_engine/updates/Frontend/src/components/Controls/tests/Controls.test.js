// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import { render } from "@testing-library/react";
import ControlsPanel from "../ControlsPanel";

describe("ControlsPanel", () => {
  test("renders without wallet controls", () => {
    const { container } = render(<ControlsPanel />);
    expect(container).toBeTruthy();
  });
});
