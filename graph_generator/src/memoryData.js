export const TOTAL_PROGRAM_MEMORY = 982;
export const TOTAL_DYNAMIC_MEMORY = 261;

export const baseData = [
  {
    name: "Program",
    used: 76,
    free: TOTAL_PROGRAM_MEMORY - 76,
  },
  {
    name: "Dynamic",
    used: 42,
    free: TOTAL_DYNAMIC_MEMORY - 42,
  },
];

export const cycleData = [
  {
    name: "Program",
    used: 292,
    free: TOTAL_PROGRAM_MEMORY - 292,
  },
  {
    name: "Dynamic",
    used: 67,
    free: TOTAL_DYNAMIC_MEMORY - 67,
  },
];

const adjustedCyclicProgramUsed = cycleData[0].used - baseData[0].used;
const adjustedCyclicDynamicUsed = cycleData[1].used - baseData[1].used;
export const adjustedCycleData = [
  {
    name: "Program",
    used: adjustedCyclicProgramUsed,
    free: TOTAL_PROGRAM_MEMORY - adjustedCyclicProgramUsed,
  },
  {
    name: "Dynamic",
    used: adjustedCyclicDynamicUsed,
    free: TOTAL_DYNAMIC_MEMORY - adjustedCyclicDynamicUsed,
  },
];

export const nnData = [
  {
    name: "Program",
    used: 236,
    free: TOTAL_PROGRAM_MEMORY - 236,
  },
  {
    name: "Dynamic",
    used: 108,
    free: TOTAL_DYNAMIC_MEMORY - 108,
  },
];

const adjustedNeuralProgramUsed = nnData[0].used - baseData[0].used;
const adjustedNeuralDynamicUsed = nnData[1].used - baseData[1].used;
export const adjustedNnData = [
  {
    name: "Program",
    used: adjustedNeuralProgramUsed,
    free: TOTAL_PROGRAM_MEMORY - adjustedNeuralProgramUsed,
  },
  {
    name: "Dynamic",
    used: adjustedNeuralDynamicUsed,
    free: TOTAL_DYNAMIC_MEMORY - adjustedNeuralDynamicUsed,
  },
];

const totalProgramUsed =
  baseData[0].used + adjustedCyclicProgramUsed + adjustedNeuralProgramUsed;

const totalDynamicUsed =
  baseData[1].used + adjustedCyclicDynamicUsed + adjustedNeuralDynamicUsed;

export const totalData = [
  {
    name: "Program",
    used: totalProgramUsed,
    free: TOTAL_PROGRAM_MEMORY - totalProgramUsed,
  },
  {
    name: "Dynamic",
    used: totalDynamicUsed,
    free: TOTAL_DYNAMIC_MEMORY - totalDynamicUsed,
  },
];

export const freeData = [
  {
    name: "Program",
    used: TOTAL_PROGRAM_MEMORY - totalProgramUsed,
    free: undefined,
  },
  {
    name: "Dynamic",
    used: TOTAL_DYNAMIC_MEMORY - totalDynamicUsed,
    free: undefined,
  },
];
