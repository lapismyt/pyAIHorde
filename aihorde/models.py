import msgspec
import enum
from typing import Optional


class AIHordeModel(msgspec.Struct):

    def to_dict(self) -> dict:
        data = {}
        for item in self.__struct_fields__:
            attr = getattr(self, item)
            if attr is None:
                continue
            if item == "post_processing":
                data["post-processing"] = attr
                continue
            if hasattr(attr, 'to_dict'):
                data[item] = attr.to_dict()
                continue
            data[item] = attr
        return msgspec.json.decode(msgspec.json.encode(data), type=dict)

    @classmethod
    def from_dict(cls, data: dict):
        kwargs = {}
        for key, value in data.items():
            if value is None:
                continue
            if key == "post-processing":
                key = "post_processing"
            kwargs[key] = value
        return msgspec.json.decode(msgspec.json.encode(kwargs), type=cls)


class Sampler(enum.StrEnum):
    k_lms = "k_lms"
    k_euler = "k_euler"
    k_euler_a = "k_euler_a"
    k_dpm_2_a = "k_dpm_2_a"
    dpmsolver = "dpmsolver"
    k_heun = "k_heun"
    k_dpmpp_2m = "k_dpmpp_2m"
    ddim = "DDIM"
    k_dpm_fast = "k_dpm_fast"
    k_dpmpp_sde = "k_dpmpp_sde"
    k_dpmpp_2s_a = "k_dpmpp_2s_a"
    k_dpm_adaptive = "k_dpm_adaptive"
    k_dpm_2 = "k_dpm_2"
    lcm = "lcm"


class PostProcessing(enum.StrEnum):
    gfpgan = "GFPGAN"
    realesrgan_x4plus = "RealESRGAN_x4plus"
    realesrgan_x2plus = "RealESRGAN_x2plus"
    realesrgan_x4plus_anime_6b = "RealESRGAN_x4plus_anime_6B"
    nmkd_siax = "NMKD_Siax"
    fourx_animesharp = "4x_AnimeSharp"
    codeformers = "CodeFormers"
    strip_background = "strip_background"


class ControlType(enum.StrEnum):
    canny = "canny"
    hed = "hed"
    depth = "depth"
    normal = "normal"
    openpose = "openpose"
    seg = "seg"
    scribble = "scribble"
    fakescribbles = "fakescribbles"
    hough = "hough"


class InjectTI(enum.StrEnum):
    prompt = "prompt"
    negprompt = "negprompt"


class SourceProcessing(enum.StrEnum):
    img2img = "img2img"
    inpainting = "inpainting"
    outpainting = "outpainting"
    remix = "remix"


class RequestWarningCode(enum.StrEnum):
    no_available_worker = "NoAvailableWorker"
    clip_skip_mismatch = "ClipSkipMismatch"
    steps_too_few = "StepsTooFew"
    steps_too_many = "StepsTooMany"
    cfg_scale_mismatch = "CfgScaleMismatch"
    cfg_scale_too_small = "CfgScaleTooSmall"
    cfg_scale_too_large = "CfgScaleTooLarge"
    sampler_mismatch = "SamplerMismatch"
    scheduler_mismatch = "SchedulerMismatch"


class GenerationStableState(enum.StrEnum):
    ok = "ok"
    censored = "censored"


class GenerationInputStableType(enum.StrEnum):
    lora = "lora"
    ti = "ti"
    censorship = "censorship"
    source_image = "source_image"
    source_mask = "source_mask"
    extra_source_images = "extra_source_images"
    batch_index = "batch_index"


class GenerationMetadataKoboldType(enum.StrEnum):
    censorship = "censorship"


class GenerationMetadataKoboldValue(enum.StrEnum):
    csam = "csam"


class GenerationMetadataStableValue(enum.StrEnum):
    download_failed = "download_failed"
    parse_failed = "parse_failed"
    baseline_mismatch = "baseline_mismatch"
    csam = "csam"
    nsfw = "nsfw"
    see_ref = "see_ref"


class WorkerDetailsType(enum.StrEnum):
    image = "image"
    text = "text"
    interrogation = "interrogation"


class GenerationKoboldState(enum.StrEnum):
    ok = "ok"
    censored = "censored"


class ModelInterrogationFormStableName(enum.StrEnum):
    caption = "caption"
    interrogation = "interrogation"
    nsfw = "nsfw"
    gfpgan = "GFPGAN"
    realesrgan_x4plus = "RealESRGAN_x4plus"
    realesrgan_x2plus = "RealESRGAN_x2plus"
    realesrgan_x4plus_anime_6b = "RealESRGAN_x4plus_anime_6B"
    nmkd_siax = "NMKD_Siax"
    fourx_animesharp = "4x_AnimeSharp"
    codeformers = "CodeFormers"
    strip_background = "strip_background"


class ActiveModelType(enum.StrEnum):
    image = "image"
    text = "text"


class ModelPayloadLorasStable(AIHordeModel):
    name: str
    model: Optional[int | float] = 1
    clip: Optional[int | float] = 1
    inject_trigger: Optional[str] = None
    is_version: Optional[bool] = False


class ModelPayloadTextualInversionsStable(AIHordeModel):
    name: str
    inject_ti: Optional[InjectTI] = None
    strength: Optional[int | float] = 1


class ExtraSourceImage(AIHordeModel):
    image: str
    strength: Optional[int | float] = 1


class ModelGenerationInputStable(AIHordeModel):
    sampler: Optional[Sampler] = Sampler.k_euler_a
    cfg_scale: Optional[int | float] = 7.5
    denoising_strength: Optional[int | float] = 1
    seed: Optional[int | str] = None
    height: Optional[int] = 512  # multiple of 64
    width: Optional[int] = 512  # multiple of 64
    seed_variation: Optional[int] = None
    post_processing: Optional[list[PostProcessing]] = None
    karras: Optional[bool] = False
    tiling: Optional[bool] = False
    hires_fix: Optional[bool] = False
    clip_skip: Optional[int] = 2
    control_type: Optional[ControlType] = None
    image_is_control: Optional[bool] = False
    return_control_map: Optional[bool] = False
    facefixer_strength: Optional[int | float] = None
    loras: Optional[list[ModelPayloadLorasStable]] = None
    tis: Optional[list[ModelPayloadTextualInversionsStable]] = None
    steps: Optional[int] = 30
    n: Optional[int] = 1


class GenerationInputStable(AIHordeModel):
    prompt: str
    params: Optional[ModelGenerationInputStable] = None
    nsfw: Optional[bool] = False
    trusted_workers: Optional[bool] = False
    slow_workers: Optional[bool] = True
    censor_nsfw: Optional[bool] = False
    workers: Optional[list[str]] = None
    worker_blacklist: Optional[bool] = False
    models: list[str] = None
    source_image: Optional[str] = None
    source_processing: Optional[SourceProcessing] = SourceProcessing.img2img
    source_mask: Optional[str] = None
    extra_source_images: Optional[list[ExtraSourceImage]] = None
    r2: Optional[bool] = True
    shared: Optional[bool] = True
    replacement_filter: Optional[bool] = True
    dry_run: Optional[bool] = False
    proxied_account: Optional[str] = None
    disable_batching: Optional[bool] = False
    allow_downgrade: Optional[bool] = False
    webhook: Optional[str] = None


class UserKudosDetails(AIHordeModel):
    accumulated: int | float = 0
    gifted: int | float = 0
    donated: int | float = 0
    admin: int | float = 0
    recieved: int | float = 0
    recurring: int | float = 0
    awarded: int | float = 0


class MonthlyKudos(AIHordeModel):
    amount: int = 0
    last_received: str = ""  # $date-time


class UsageDetails(AIHordeModel):
    megapixelsteps: int | float = 0
    requests: int = 0


class ContributionsDetails(AIHordeModel):
    megapixelsteps: int | float = 0
    fulfillments: int = 0


class UserThingRecords(AIHordeModel):
    megapixelsteps: int | float = 0
    tokens: int = 0


class UserAmountRecords(AIHordeModel):
    image: int = 0
    text: int = 0
    interrogation: int = 0


class UserRecords(AIHordeModel):
    usage: UserThingRecords = None
    contribution: UserThingRecords = None
    fulfillment: UserAmountRecords = None
    request: UserAmountRecords = None


class UserDetails(AIHordeModel):
    username: str
    id: int
    kudos: int | float = 0
    evaluating_kudos: int | float = 0
    concurrency: int = 0
    worker_invited: int = 0
    moderator: bool = False
    kudos_details: UserKudosDetails = None
    worker_count: int = 0
    worker_ids: list[str] = []
    sharedkey_ids: list[str] = []
    monthly_kudos: MonthlyKudos = None
    trusted: bool = False
    flagged: bool = False
    vpn: bool = False
    service: bool = False
    suspicious: int = 0
    pseudonymous: bool = False
    contact: Optional[str] = None
    admin_comment: Optional[str] = None
    account_age: int = 0
    usage: UsageDetails = None
    contributions: ContributionsDetails = None
    records: UserRecords = None


class RequestSingleWarning(AIHordeModel):
    code: RequestWarningCode = None
    message: str = None


class RequestAsync(AIHordeModel):
    id: str
    kudos: int | float = 0
    message: Optional[str] = None
    warnings: Optional[list[RequestSingleWarning]] = None


class RequestStatusCheck(AIHordeModel):
    finished: int = 0
    processing: int = 0
    restarted: int = 0
    waiting: int = 0
    done: bool = False
    falted: Optional[bool] = False
    wait_time: int = 0
    queue_position: int = 0
    kudos: int | float = 0
    is_possible: Optional[bool] = True


class GenerationMetadataStable(AIHordeModel):
    type: GenerationInputStableType
    value: GenerationMetadataStableValue
    ref: Optional[str] = None


class GenerationStable(AIHordeModel):
    worker_id: str = None
    worker_name: str = None
    model: str = None
    state: GenerationStableState = GenerationStableState.ok
    img: str = None
    seed: str = None
    id: str = None
    censored: bool = False
    gen_metadata: Optional[list[GenerationMetadataStable]] = None


class RequestStatusStable(AIHordeModel):
    finished: int = 0
    processing: int = 0
    restarted: int = 0
    waiting: int = 0
    done: bool = False
    faulted: Optional[bool] = False
    wait_time: int = 0
    queue_position: int = 0
    kudos: int | float = 0
    is_possible: Optional[bool] = True
    generations: list[GenerationStable] = []
    shared: bool = False


class ModelGenerationInputKobold(AIHordeModel):
    n: Optional[int] = 1

    # pls dont be scared, it's formatting options, check https://aihorde.net/api
    frmtadsnsp: Optional[bool] = None
    frmtrmspch: Optional[bool] = None
    frmttriminc: Optional[bool] = None

    max_context_length: Optional[int] = 1024
    max_length: Optional[int] = 80
    rep_pen: Optional[int | float] = None
    rep_pen_range: Optional[int] = None
    rep_pen_slope: Optional[int | float] = None

    singleline: Optional[bool] = False
    temperature: Optional[int | float] = None
    tfs: Optional[int | float] = None
    top_a: Optional[int | float] = None
    top_k: Optional[int] = None
    top_p: Optional[int | float] = None
    typical: Optional[int | float] = None
    sampler_order: Optional[list[int]] = None
    use_default_badwordsids: Optional[bool] = None
    stop_sequence: Optional[list[str]] = None
    min_p: Optional[int | float] = 0
    smoothing_factor: Optional[int | float] = 0
    dynatemp_range: Optional[int | float] = 0
    dynatemp_exponent: Optional[int | float] = 1


class GenerationInputKobold(AIHordeModel):
    prompt: str
    params: Optional[ModelGenerationInputKobold] = None
    softprompt: Optional[str] = None
    trusted_workers: Optional[bool] = False
    slow_workers: Optional[bool] = True
    workers: Optional[list[str]] = None
    worker_blacklist: Optional[bool] = False
    models: Optional[list[str]] = None
    dry_run: Optional[bool] = False
    proxied_account: Optional[str] = None
    extra_source_images: Optional[list[ExtraSourceImage]] = None
    disable_batching: Optional[bool] = False
    allow_downgrade: Optional[bool] = False
    webhook: Optional[str] = None


class GenerationMetadataKobold(AIHordeModel):
    type: GenerationMetadataKoboldType
    value: GenerationMetadataKoboldValue
    ref: Optional[str] = None


class GenerationKobold(AIHordeModel):
    state: GenerationKoboldState
    worker_id: Optional[str] = None
    worker_name: Optional[str] = None
    model: Optional[str] = None
    text: Optional[str] = None
    seed: Optional[int] = None
    gen_metadata: Optional[list[GenerationMetadataKobold]] = None


class RequestStatusKobold(AIHordeModel):
    finished: Optional[int] = None
    processing: Optional[int] = None
    restarted: Optional[int] = None
    waiting: Optional[int] = None
    done: Optional[bool] = None
    faulted: Optional[bool] = None
    wait_time: Optional[int] = None
    queue_position: Optional[int] = None
    kudos: Optional[int | float] = None
    is_possible: Optional[bool] = None
    generations: Optional[list[GenerationKobold]] = None


class ModelInterrogationFormPayloadStable(dict):
    pass


class InterrogationFormResult(dict):
    pass


class ModelInterrogationFormStable(AIHordeModel):
    name: ModelInterrogationFormStableName
    payload: Optional[ModelInterrogationFormPayloadStable] = None


class ModelInterrogationInputStable(AIHordeModel):
    forms: list[ModelInterrogationFormStable]
    source_image: str
    slow_workers: Optional[bool] = True
    webhook: Optional[str] = None


class RequestInterrogationResponse(AIHordeModel):
    id: str
    message: Optional[str] = None


class InterrogationFormStatus(AIHordeModel):
    form: str
    state: Optional[str] = None
    result: Optional[InterrogationFormResult] = None


class InterrogationStatus(AIHordeModel):
    state: Optional[str] = None
    forms: Optional[list[InterrogationFormStatus]] = None


class ActiveModel(AIHordeModel):
    name: str
    count: int
    performance: int | float
    queued: int | float
    jobs: int | float
    eta: int
    type: ActiveModelType


class Newspiece(AIHordeModel):
    date_published: str
    newspiece: str
    importance: str


class HordePerformance(AIHordeModel):
    queued_requests: int
    queued_text_requests: int
    worker_count: int
    text_worker_count: int
    thread_count: int
    text_thread_count: int
    queued_megapixelsteps: int | float
    past_minute_megapixelsteps: int | float
    queued_forms: int | float
    interrogator_count: int
    interrogator_thread_count: int
    queued_tokens: int | float
    past_minute_tokens: int | float


class WorkerKudosDetails(AIHordeModel):
    generated: int | float = 0
    uptime: int = 0


class TeamDetailsLite(AIHordeModel):
    name: str = None
    id: str = None


class WorkerDetails(AIHordeModel):
    type: WorkerDetailsType = WorkerDetailsType.image
    name: str = None
    id: str = None
    online: bool = False
    requests_fulfilled: int = 0
    kudos_rewards: int | float = 0
    kudos_details: WorkerKudosDetails = None
    performance: str = None
    threads: int = 0
    uptime: int = None
    maintenance_mode: bool = False
    paused: bool = False
    info: str = None
    nsfw: bool = False
    owner: str = None
    ipaddr: str = None
    trusted: bool = False
    flagged: bool = False
    suspicious: int = 0
    uncompleted_jobs: int = 0
    models: list[str] = []
    forms: list[str] = []
    team: TeamDetailsLite = None
    contact: str = None
    bridge_agent: str = "unknown:0:unknown"
    max_pixels: int = 0
    megapixelsteps_generated: int | float = 0
    img2img: bool = False
    painting: bool = False
    post_processing: bool = False
    lora: bool = False
    max_length: int = 0
    max_context_length: int = 0
    tokens_generated: int | float = 0
